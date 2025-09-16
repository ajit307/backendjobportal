# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    job_seeker = "job_seeker"
    employer = "employer"
    admin = "admin"

class ExperienceLevel(str, Enum):
    entry = "entry"
    mid = "mid"
    senior = "senior"

class ApplicationStatus(str, Enum):
    pending = "pending"
    shortlisted = "shortlisted"
    rejected = "rejected"

# User
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

# Job
class JobBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[float] = 0
    salary_max: Optional[float] = 0
    required_skills: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None

class JobCreate(JobBase):
    pass

class JobOut(JobBase):
    id: int
    employer_id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

# Application
class ApplicationBase(BaseModel):
    cover_letter: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    job_id: int

class ApplicationOut(ApplicationBase):
    id: int
    job_id: int
    candidate_id: int
    status: ApplicationStatus
    applied_at: datetime

    class Config:
        orm_mode = True
