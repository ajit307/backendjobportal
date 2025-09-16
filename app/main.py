# app/main.py

from fastapi import FastAPI
from app.db.session import Base, engine
from app.routers import auth
from app.routers import auth, users, jobs, applications, admin




# Create database tables (development only; for production, use Alembic migrations)
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Job Portal Backend")

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(admin.router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Job Portal Backend is running!"}
