# Mini Resume Management API

## Python Version Used
Python 3.12.3

---

## Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/Sadiq2678/miniresume-Mohammed-Sadiq.git
cd miniresume-Mohammed-Sadiq
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Steps to Run the Application

Start the FastAPI server using:

```bash
uvicorn main:app --reload
```

The application will be available at:

```
http://127.0.0.1:8000
```

---

## Example API Requests and Responses

### Health Check

**Request**

```http
GET /health
```

**Response**

```json
{
  "status": "ok"
}
```

---

### Create Candidate (Upload Resume)

**Request**

```http
POST /candidates
Content-Type: multipart/form-data
```

**Form Data**

```
full_name=John Doe
dob=1998-05-20
contact_number=9876543210
contact_address=Chennai, India
education=B.Tech Computer Science
graduation_year=2020
experience_years=3
skills=python,fastapi
resume=resume.pdf
```

**Response**

```json
{
  "id": "8c2e9c6b-1c2a-4e8b-9a3d-7b6c9e2f4a11",
  "full_name": "John Doe",
  "dob": "1998-05-20",
  "contact_number": "9876543210",
  "contact_address": "Chennai, India",
  "education": "B.Tech Computer Science",
  "graduation_year": 2020,
  "experience_years": 3,
  "skills": ["python", "fastapi"],
  "resume_filename": "8c2e9c6b-1c2a-4e8b-9a3d-7b6c9e2f4a11_resume.pdf"
}
```

---

### List Candidates (With Filters)

**Request**

```http
GET /candidates?skill=python&experience=3
```

**Response**

```json
[
  {
    "id": "8c2e9c6b-1c2a-4e8b-9a3d-7b6c9e2f4a11",
    "full_name": "John Doe",
    "dob": "1998-05-20",
    "contact_number": "9876543210",
    "contact_address": "Chennai, India",
    "education": "B.Tech Computer Science",
    "graduation_year": 2020,
    "experience_years": 3,
    "skills": ["python", "fastapi"],
    "resume_filename": "8c2e9c6b-1c2a-4e8b-9a3d-7b6c9e2f4a11_resume.pdf"
  }
]
```

---

### Get Candidate by ID

**Request**

```http
GET /candidates/8c2e9c6b-1c2a-4e8b-9a3d-7b6c9e2f4a11
```

**Response**

```json
{
  "id": "8c2e9c6b-1c2a-4e8b-9a3d-7b6c9e2f4a11",
  "full_name": "John Doe",
  "dob": "1998-05-20",
  "contact_number": "9876543210",
  "contact_address": "Chennai, India",
  "education": "B.Tech Computer Science",
  "graduation_year": 2020,
  "experience_years": 3,
  "skills": ["python", "fastapi"],
  "resume_filename": "8c2e9c6b-1c2a-4e8b-9a3d-7b6c9e2f4a11_resume.pdf"
}
```

---

### Delete Candidate

**Request**

```http
DELETE /candidates/8c2e9c6b-1c2a-4e8b-9a3d-7b6c9e2f4a11
```

**Response**

```json
{
  "message": "Candidate and resume deleted successfully"
}


