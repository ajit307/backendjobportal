# app/crud.py
from sqlalchemy.orm import Session
from app import models, schemas
from app.utils.security import hash_password

# Users
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Jobs
def create_job(db: Session, job: schemas.JobCreate, employer_id: int):
    db_job = models.Job(**job.dict(), employer_id=employer_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id, models.Job.is_active==True).first()

def list_jobs(db: Session, skip: int =0, limit:int=100, filters:dict=None):
    q = db.query(models.Job).filter(models.Job.is_active==True)
    if filters:
        if "keyword" in filters:
            kw = f"%{filters['keyword']}%"
            q = q.filter((models.Job.title.ilike(kw)) | (models.Job.description.ilike(kw)))
        if "location" in filters:
            q = q.filter(models.Job.location.ilike(f"%{filters['location']}%"))
        if "experience_level" in filters:
            q = q.filter(models.Job.experience_level == filters["experience_level"])
        if "min_salary" in filters:
            q = q.filter(models.Job.salary_min >= filters["min_salary"])
        if "max_salary" in filters:
            q = q.filter(models.Job.salary_max <= filters["max_salary"])
    return q.offset(skip).limit(limit).all()

# Applications
def apply_to_job(db: Session, application: schemas.ApplicationCreate, candidate_id: int):
    # check duplicate application
    existing = db.query(models.Application).filter(
        models.Application.job_id == application.job_id,
        models.Application.candidate_id == candidate_id
    ).first()
    if existing:
        return None
    db_app = models.Application(
        job_id=application.job_id,
        candidate_id=candidate_id,
        cover_letter=application.cover_letter
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def list_applications_for_job(db: Session, job_id: int):
    return db.query(models.Application).filter(models.Application.job_id==job_id).all()


