# app/routers/applications.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models
from app.deps import get_db, require_role, get_current_user

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=schemas.ApplicationOut)
def apply(application_in: schemas.ApplicationCreate, db: Session = Depends(get_db), current_user = Depends(require_role("job_seeker"))):
    app_obj = crud.apply_to_job(db, application_in, candidate_id=current_user.id)
    if app_obj is None:
        raise HTTPException(status_code=400, detail="Already applied")
    return app_obj

@router.get("/me", response_model=List[schemas.ApplicationOut])
def my_applications(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(models.Application).filter(models.Application.candidate_id==current_user.id).all()

@router.get("/job/{job_id}", response_model=List[schemas.ApplicationOut])
def get_applications_for_job(job_id:int, db: Session = Depends(get_db), current_user = Depends(require_role("employer"))):
    # employer can view only if they own the job
    job = db.query(models.Job).filter(models.Job.id==job_id).first()
    if not job or job.employer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    return crud.list_applications_for_job(db, job_id)
