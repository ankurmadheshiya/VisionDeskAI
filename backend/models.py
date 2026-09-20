from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))

class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    violation_type = Column(String(100), index=True)
    severity = Column(String(50), default="High")  # Critical, High, Medium, Low
    status = Column(String(50), default="Open")     # Open, Investigating, Resolved
    location = Column(String(100), default="Construction Bay A")
    department = Column(String(100), default="Safety & Compliance")
    confidence = Column(Float, default=0.92)
    evidence_url = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(Text, nullable=True)

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    location = Column(String(100))
    department = Column(String(100))
    severity = Column(String(50))
    status = Column(String(50), default="Reported")
    reported_by = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)

class DetectionResult(Base):
    __tablename__ = "detection_results"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255))
    media_type = Column(String(50))  # image, video
    total_workers = Column(Integer, default=0)
    detected_ppe = Column(Text)       # JSON string or comma list
    missing_ppe = Column(Text)        # JSON string or comma list
    confidence = Column(Float, default=0.90)
    output_image_path = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class InvestigationCase(Base):
    __tablename__ = "investigation_cases"

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(50), unique=True, index=True)
    title = Column(String(200))
    status = Column(String(50), default="In Progress")
    assigned_to = Column(String(100), default="Safety Investigator AI")
    query = Column(Text)
    findings = Column(Text, nullable=True)
    human_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ReportRecord(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    report_type = Column(String(100))  # Incident, Violation, Compliance, Monthly
    format = Column(String(20))         # CSV, Excel, PDF
    file_path = Column(String(255))
    generated_at = Column(DateTime, default=datetime.utcnow)
