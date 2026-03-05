from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import uuid
import os

# ---------------------
# Database Setup (SQLite — no installation required)
# ---------------------
DATABASE_URL = "sqlite:///./resume.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------
# ORM Model
# ---------------------
class CandidateDB(Base):
    __tablename__ = "candidates"

    id               = Column(String, primary_key=True, index=True)
    full_name        = Column(String, nullable=False)
    dob              = Column(Date,   nullable=False)
    contact_number   = Column(String, nullable=False)
    contact_address  = Column(String, nullable=False)
    education        = Column(String, nullable=False)
    graduation_year  = Column(Integer, nullable=False)
    experience_years = Column(Integer, nullable=False)
    skills           = Column(String,  nullable=False)  # stored as comma-separated string
    resume_filename  = Column(String,  nullable=False)


Base.metadata.create_all(bind=engine)

# ---------------------
# FastAPI App
# ---------------------
app = FastAPI(title="Mini Resume Management API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


# ---------------------
# Pydantic Schema
# ---------------------
class CandidateResponse(BaseModel):
    id:               str
    full_name:        str
    dob:              date
    contact_number:   str
    contact_address:  str
    education:        str
    graduation_year:  int
    experience_years: int
    skills:           List[str]
    resume_filename:  str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_model(cls, obj: CandidateDB) -> "CandidateResponse":
        return cls(
            id=obj.id,
            full_name=obj.full_name,
            dob=obj.dob,
            contact_number=obj.contact_number,
            contact_address=obj.contact_address,
            education=obj.education,
            graduation_year=obj.graduation_year,
            experience_years=obj.experience_years,
            skills=[s.strip() for s in obj.skills.split(",") if s.strip()],
            resume_filename=obj.resume_filename,
        )


# ---------------------
# Health Check
# ---------------------
@app.get("/health", status_code=200)
def health():
    """Health check endpoint."""
    return {"status": "ok"}


# ---------------------
# Upload Resume / Create Candidate
# ---------------------
@app.post("/candidates", response_model=CandidateResponse, status_code=201)
async def create_candidate(
    full_name:        str  = Form(..., description="Full name of the candidate"),
    dob:              date = Form(..., description="Date of birth (YYYY-MM-DD)"),
    contact_number:   str  = Form(..., description="Contact phone number"),
    contact_address:  str  = Form(..., description="Contact address"),
    education:        str  = Form(..., description="Highest education qualification"),
    graduation_year:  int  = Form(..., ge=1900, le=2100, description="Year of graduation"),
    experience_years: int  = Form(..., ge=0,    description="Years of work experience"),
    skills:           str  = Form(..., description="Comma-separated skill set (e.g. Python,Django,SQL)"),
    resume:           UploadFile = File(..., description="Resume file (PDF / DOC / DOCX)"),
    db:               Session = Depends(get_db),
):
    """Upload a resume and store candidate metadata."""
    if resume.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF, DOC, and DOCX are accepted.",
        )

    candidate_id = str(uuid.uuid4())
    filename     = f"{candidate_id}_{resume.filename}"
    file_path    = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(await resume.read())

    normalized_skills = ",".join(s.strip().lower() for s in skills.split(",") if s.strip())

    candidate = CandidateDB(
        id=candidate_id,
        full_name=full_name,
        dob=dob,
        contact_number=contact_number,
        contact_address=contact_address,
        education=education,
        graduation_year=graduation_year,
        experience_years=experience_years,
        skills=normalized_skills,
        resume_filename=filename,
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return CandidateResponse.from_orm_model(candidate)


# ---------------------
# List Candidates (with filters)
# ---------------------
@app.get("/candidates", response_model=List[CandidateResponse])
def list_candidates(
    skill:           Optional[str] = None,
    experience:      Optional[int] = None,
    graduation_year: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    List all candidates.
    Optionally filter by skill, experience (years), or graduation_year.
    """
    query = db.query(CandidateDB)

    if experience is not None:
        query = query.filter(CandidateDB.experience_years == experience)

    if graduation_year is not None:
        query = query.filter(CandidateDB.graduation_year == graduation_year)

    results = query.all()

    if skill:
        skill_lower = skill.strip().lower()
        results = [c for c in results if skill_lower in [s.strip() for s in c.skills.split(",")]]

    return [CandidateResponse.from_orm_model(c) for c in results]


# ---------------------
# Get Candidate by ID
# ---------------------
@app.get("/candidates/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: str, db: Session = Depends(get_db)):
    """Fetch a single candidate by their ID."""
    candidate = db.query(CandidateDB).filter(CandidateDB.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return CandidateResponse.from_orm_model(candidate)


# ---------------------
# Delete Candidate
# ---------------------
@app.delete("/candidates/{candidate_id}", status_code=200)
def delete_candidate(candidate_id: str, db: Session = Depends(get_db)):
    """Delete a candidate and their uploaded resume file."""
    candidate = db.query(CandidateDB).filter(CandidateDB.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    file_path = os.path.join(UPLOAD_DIR, candidate.resume_filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(candidate)
    db.commit()
    return {"message": "Candidate deleted successfully"}