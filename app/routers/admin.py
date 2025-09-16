# app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.deps import get_db, require_role

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db), current_user = Depends(require_role("admin"))):
    return db.query(models.User).all()

@router.post("/users/{user_id}/deactivate")
def deactivate_user(user_id:int, db: Session = Depends(get_db), current_user = Depends(require_role("admin"))):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.add(user)
    db.commit()
    return {"detail":"User deactivated"}

@router.get("/jobs")
def list_all_jobs(db: Session = Depends(get_db), current_user = Depends(require_role("admin"))):
    return db.query(models.Job).all()

@router.get("/applications")
def list_all_applications(db: Session = Depends(get_db), current_user = Depends(require_role("admin"))):
    return db.query(models.Application).all()
