from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import schemas
from .models import course_models as models
from .database import get_db, engine, Base

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/courses", response_model=list[schemas.CourseRead])
def get_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

