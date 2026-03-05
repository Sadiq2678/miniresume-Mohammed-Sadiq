# Mini Resume Management API

A REST API built with **FastAPI** for collecting, storing, and searching candidate resume data.

---

## Python Version

**Python 3.11+**

---

## Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/Sadiq2678/miniresume-Mohammed-Sadiq.git
cd miniresume-Mohammed-Sadiq

# 2. Create and activate a virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Steps to Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at: **http://localhost:8000**  
Interactive Swagger docs: **http://localhost:8000/docs**

> No database setup needed — the app uses SQLite and creates `resume.db` automatically on first run.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/candidates` | Upload resume + store candidate |
| GET | `/candidates` | List candidates (supports filters) |
| GET | `/candidates/{id}` | Get candidate by ID |
| DELETE | `/candidates/{id}` | Delete candidate + resume file |

### Filter Query Parameters for `GET /candidates`

| Parameter | Type | Example |
|-----------|------|---------|
| `skill` | string | `?skill=python` |
| `experience` | integer | `?experience=3` |
| `graduation_year` | integer | `?graduation_year=2022` |

---

## Example API Requests & Responses

### Health Check

**Request**
```
GET /health
```
**Response** `200 OK`
```json
{
  "status": "ok"
}
```

---

### Upload Resume (Create Candidate)

**Request** — multipart/form-data
```
POST /candidates
```

| Field | Type | Example |
|-------|------|---------|
| full_name | string | John Doe |
| dob | date | 1998-05-15 |
| contact_number | string | +91-9876543210 |
| contact_address | string | Chennai, Tamil Nadu |
| education | string | B.Tech Computer Science |
| graduation_year | integer | 2020 |
| experience_years | integer | 3 |
| skills | string | python,django,sql |
| resume | file | resume.pdf |

**Response** `201 Created`
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "full_name": "John Doe",
  "dob": "1998-05-15",
  "contact_number": "+91-9876543210",
  "contact_address": "Chennai, Tamil Nadu",
  "education": "B.Tech Computer Science",
  "graduation_year": 2020,
  "experience_years": 3,
  "skills": ["python", "django", "sql"],
  "resume_filename": "a1b2c3d4-e5f6-7890-abcd-ef1234567890_resume.pdf"
}
```

---

### List Candidates with Filters

**Request**
```
GET /candidates?skill=python&experience=3
```

**Response** `200 OK`
```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "full_name": "John Doe",
    "dob": "1998-05-15",
    "contact_number": "+91-9876543210",
    "contact_address": "Chennai, Tamil Nadu",
    "education": "B.Tech Computer Science",
    "graduation_year": 2020,
    "experience_years": 3,
    "skills": ["python", "django", "sql"],
    "resume_filename": "a1b2c3d4-e5f6-7890-abcd-ef1234567890_resume.pdf"
  }
]
```

---

### Get Candidate by ID

**Request**
```
GET /candidates/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Response** `200 OK`
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "full_name": "John Doe",
  ...
}
```

**Not found** `404`
```json
{ "detail": "Candidate not found" }
```

---

### Delete Candidate

**Request**
```
DELETE /candidates/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Response** `200 OK`
```json
{ "message": "Candidate deleted successfully" }
```

---

## Project Structure

```
miniresume-your-full-name/
├── main.py            # All routes, DB models, and app logic
├── requirements.txt   # Python dependencies
├── README.md          # This file
├── .gitignore
└── uploads/           # Resume files (auto-created, git-ignored)
```

---

## Notes

- Resume files (PDF/DOC/DOCX) are saved in the `uploads/` folder.
- The SQLite database (`resume.db`) is auto-created — no setup required.
- Skills are stored in lowercase and matched case-insensitively.