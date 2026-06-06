import shutil
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from app.db.dependency import get_db
from app.models.application import Application
from app.models.job import Job
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter()


@router.post("/apply/{job_id}")
def apply_job(
    job_id: int,
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    existing_application = db.query(Application).filter(
        Application.user_id == current_user.id,
        Application.job_id == job_id
    ).first()

    if existing_application:
        raise HTTPException(status_code=400, detail="Already applied")

    # Save file physically
    upload_folder = "uploads"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = f"{upload_folder}/{resume.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    # Save in DB
    new_application = Application(
        user_id=current_user.id,
        job_id=job_id,
        resume=resume.filename
    )

    db.add(new_application)
    db.commit()

    return {
        "message": "Applied successfully",
        "resume_saved_as": resume.filename
    }
@router.get("/all")
def get_all_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    applications = db.query(Application).all()

    result = []

    for app in applications:
        result.append({
            "application_id": app.id,
            "applicant": app.user.username,
            "email": app.user.email,
            "job_title": app.job.title,
            "company": app.job.company,
            "resume": app.resume,
            "status": app.status
        })

    return result
@router.get("/my-applications")
def my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    applications = db.query(Application).filter(
        Application.user_id == current_user.id
    ).all()

    result = []

    for app in applications:

        result.append({
            "application_id": app.id,
            "job_title": app.job.title,
            "company": app.job.company,
            "resume": app.resume,
            "status": app.status
        })

    return result
@router.get("/download-resume/{filename}")
def download_resume(
    filename: str,
    current_user: User = Depends(get_current_user)
):

    file_path = f"uploads/{filename}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )
@router.put("/status/{application_id}")
def update_application_status(
    application_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    application = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    application.status = status

    db.commit()

    return {
        "message": f"Application {status}"
    }