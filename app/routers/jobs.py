# app/routers/jobs.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app import schemas, crud, models
from app.deps import get_db, require_role, get_current_user

# Make sure router is defined exactly like this
router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/", response_model=schemas.JobOut)
def create_job(
    job_in: schemas.JobCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("employer"))
):
    return crud.create_job(db, job_in, employer_id=current_user.id)

@router.get("/", response_model=List[schemas.JobOut])
def list_jobs(
    skip: int = 0,
    limit: int = 20,
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    experience_level: Optional[models.ExperienceLevel] = None,
    min_salary: Optional[float] = None,
    max_salary: Optional[float] = None,
    db: Session = Depends(get_db)
):
    filters = {}
    if keyword:
        filters["keyword"] = keyword
    if location:
        filters["location"] = location
    if experience_level:
        filters["experience_level"] = experience_level
    if min_salary is not None:
        filters["min_salary"] = min_salary
    if max_salary is not None:
        filters["max_salary"] = max_salary
    return crud.list_jobs(db, skip=skip, limit=limit, filters=filters)

@router.get("/{job_id}", response_model=schemas.JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.patch("/{job_id}")
def update_job(
    job_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("employer"))
):
    job = crud.get_job(db, job_id)
    if not job or job.employer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found or permission denied")
    for k, v in payload.items():
        setattr(job, k, v)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job
