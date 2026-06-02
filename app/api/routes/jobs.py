from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependency import get_db
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate
from app.core.deps import get_current_user
from app.models.application import Application


router = APIRouter()


@router.post("/create")
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_job = Job(
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "Job created successfully",
        "created_by": current_user.email,
        "job_id": new_job.id
    }


@router.get("/")
def get_jobs(db: Session = Depends(get_db)):

    jobs = db.query(Job).all()

    return jobs
@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully"
    }
@router.put("/{job_id}")
def update_job(
    job_id: int,
    updated_job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    job.title = updated_job.title
    job.company = updated_job.company
    job.location = updated_job.location
    job.description = updated_job.description

    db.commit()

    return {
        "message": "Job updated successfully"
    }
@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db)
):

    total_jobs = db.query(Job).count()

    total_applications = db.query(Application).count()

    total_users = db.query(User).count()

    return {
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "total_users": total_users
    }