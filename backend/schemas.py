from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class ViolationCreate(BaseModel):
    violation_type: str
    severity: str = "High"
    status: str = "Open"
    location: str = "Construction Bay A"
    department: str = "Safety & Compliance"
    confidence: float = 0.92
    evidence_url: Optional[str] = None
    details: Optional[str] = None

class ViolationResponse(BaseModel):
    id: int
    violation_type: str
    severity: str
    status: str
    location: str
    department: str
    confidence: float
    evidence_url: Optional[str]
    timestamp: datetime
    details: Optional[str]

    class Config:
        from_attributes = True

class IncidentCreate(BaseModel):
    title: str
    description: str
    location: str
    department: str
    severity: str = "High"
    reported_by: str = "Safety Inspector"

class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    department: str
    severity: str
    status: str
    reported_by: str
    timestamp: datetime

    class Config:
        from_attributes = True

class MultimodalInsightRequest(BaseModel):
    visual_violation: str
    location: Optional[str] = "Site A"
    department: Optional[str] = "Construction"
    collection_name: str = "pdf_documents"

class InvestigationRequest(BaseModel):
    incident_title: str
    incident_details: str
    location: Optional[str] = "Site A"
    department: Optional[str] = "Operations"
