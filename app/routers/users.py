# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.deps import get_db, get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schemas.UserOut)
def read_me(current_user = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=schemas.UserOut)
def update_profile(payload: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # simple update for full_name only example
    if "full_name" in payload:
        current_user.full_name = payload["full_name"]
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
    return current_user

@router.delete("/me")
def delete_me(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    current_user.is_active = False
    db.add(current_user)
    db.commit()
    return {"detail": "Account deactivated"}
