from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import date
import uuid
import os

app = FastAPI()

# In-memory storage
candidates: Dict[str, dict] = {}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -----------------------
# Models
# -----------------------
class CandidateResponse(BaseModel):
    id: str
    full_name: str
    dob: date
    contact_number: str
    contact_address: str
    education: str
    graduation_year: int
    experience_years: int
    skills: List[str]
    resume_filename: str


# -----------------------
# Health Check
# -----------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------
# Upload Resume
# -----------------------
@app.post("/candidates", response_model=CandidateResponse)
async def create_candidate(
    full_name: str = Form(...),
    dob: date = Form(...),
    contact_number: str = Form(...),
    contact_address: str = Form(...),
    education: str = Form(...),
    graduation_year: int = Form(..., ge=1900),
    experience_years: int = Form(..., ge=0),
    skills: str = Form(...),  # comma-separated
    resume: UploadFile = File(...)
):
    if resume.content_type not in [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]:
        raise HTTPException(status_code=400, detail="Invalid resume file type")

    candidate_id = str(uuid.uuid4())
    filename = f"{candidate_id}_{resume.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(await resume.read())

    candidate = {
        "id": candidate_id,
        "full_name": full_name,
        "dob": dob,
        "contact_number": contact_number,
        "contact_address": contact_address,
        "education": education,
        "graduation_year": graduation_year,
        "experience_years": experience_years,
        "skills": [s.strip().lower() for s in skills.split(",")],
        "resume_filename": filename
    }

    candidates[candidate_id] = candidate
    return candidate


# -----------------------
# List Candidates (filters)
# -----------------------
@app.get("/candidates", response_model=List[CandidateResponse])
def list_candidates(
    skill: str | None = None,
    experience: int | None = None,
    graduation_year: int | None = None
):
    result = list(candidates.values())

    if skill:
        result = [c for c in result if skill.lower() in c["skills"]]

    if experience is not None:
        result = [c for c in result if c["experience_years"] == experience]

    if graduation_year is not None:
        result = [c for c in result if c["graduation_year"] == graduation_year]

    return result


# -----------------------
# Get Candidate by ID
# -----------------------
@app.get("/candidates/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: str):
    candidate = candidates.get(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


# -----------------------
# Delete Candidate
# -----------------------
@app.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id: str):
    candidate = candidates.get(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Remove resume file
    file_path = os.path.join(UPLOAD_DIR, candidate["resume_filename"])
    if os.path.exists(file_path):
        os.remove(file_path)

    # Remove candidate from memory
    candidates.pop(candidate_id)

    return {"message": "Candidate and resume deleted successfully"}
