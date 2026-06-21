# 🚀 Smart Job Portal Backend

A FastAPI-powered backend for a Smart Job Portal that helps job seekers apply for jobs, receive ATS-based resume analysis, track applications, and attend scheduled interviews while allowing recruiters to manage candidates efficiently.

---

## 📌 Features

### 🔐 Authentication

* User Registration
* User Login
* JWT Authentication
* Protected Routes

### 💼 Job Management

* Create Jobs
* View Jobs
* Filter Jobs by Category
* Manage Job Listings

### 📄 Application Management

* Apply for Jobs
* Resume Upload
* Application Status Tracking
* ATS Resume Analysis

### 🤖 ATS Resume Analyzer

* Resume Skill Extraction
* ATS Score Calculation
* Missing Skills Detection
* Improvement Suggestions

### 🎤 Interview Management

* Schedule Interviews
* View Scheduled Interviews
* Interview Status Tracking
* Meeting Link Integration

### 📧 Email Notifications

* Interview Scheduling Notifications
* Application Updates

### 📊 Analytics

* Total Jobs
* Total Applications
* Accepted Candidates
* Rejected Candidates
* Pending Applications

---

## 🛠️ Tech Stack

| Technology | Purpose              |
| ---------- | -------------------- |
| FastAPI    | Backend Framework    |
| Python     | Programming Language |
| SQLAlchemy | ORM                  |
| MySQL      | Database             |
| JWT        | Authentication       |
| Pydantic   | Validation           |
| Uvicorn    | ASGI Server          |

---

## 📂 Project Structure

backend/

├── app/

│ ├── api/

│ ├── core/

│ ├── db/

│ ├── models/

│ ├── schemas/

│ ├── services/

│

├── uploads/

├── requirements.txt

├── main.py

---

## ⚙️ Installation

### Clone Repository

git clone https://github.com/brahmmareddy-123/smart_job_portal_backend.git

cd smart_job_portal_backend

### Create Virtual Environment

python -m venv venv

### Activate Environment

Windows:

venv\Scripts\activate

### Install Dependencies

pip install -r requirements.txt

### Run Server

uvicorn app.main:app --reload

---

## 📚 API Documentation

Swagger Documentation:

http://localhost:8000/docs

---

## 🔮 Future Improvements

* Company-specific recruiter accounts
* AI candidate ranking
* Real-time notifications
* Video interview integration
* Advanced analytics dashboard

---

## 👨‍💻 Author

**Bandi Brahmma Reddy**
