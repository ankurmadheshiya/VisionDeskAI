from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import engine, get_db
from backend.models import Base, User
from backend.schemas import UserCreate, UserLogin
from backend.auth import hash_password, verify_password

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "VisionDesk API is running"}


@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    try:
        from sqlalchemy import text
        # Execute simple query to test DB connection
        db.execute(text("SELECT 1"))
        return {"status": "connected", "database": "sqlite"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )


# ---------------------- SIGNUP ---------------------- #
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = hash_password(user.password)

    # Create new user
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }


# ---------------------- LOGIN ---------------------- #
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    # Find user by email
    existing_user = db.query(User).filter(User.email == user.email).first()

    # Check if user exists
    if not existing_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid Email or Password"
        )

    # Verify password
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid Email or Password"
        )

    return {
        "message": "Login Successful",
        "name": existing_user.name,
        "email": existing_user.email
    }