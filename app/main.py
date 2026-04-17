from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, joinedload
from . import schemas
from .models import course_models as models
from .database import get_db, engine
from sqlalchemy import or_, distinct

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Route to test connections
@app.get("/")
def root():
    return {"Hello": "World"}


# Retrieves all courses
@app.get("/courses", response_model=list[schemas.CourseRead])
def get_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()


# Retrieves all subjects
@app.get("/subjects", response_model=list[str])
def get_subjects(db: Session = Depends(get_db)):
    subjects = db.query(distinct(models.Course.subject)).all()
    return [s[0] for s in subjects]


# Retrieves all courses that match an id or title query
@app.get("/courses/search", response_model=list[schemas.SectionRead])
def search_courses(
        query: str,
        db: Session = Depends(get_db)
):
    results = (
        db.query(models.Section)
        .join(models.Course)
        .options(
            joinedload(models.Section.course),
            joinedload(models.Section.semester),
            joinedload(models.Section.meetings)
            .joinedload(models.Meeting.instructors)
            .joinedload(models.MeetingInstructor.instructor),
            joinedload(models.Section.meetings)
            .joinedload(models.Meeting.meeting_days),
        )
        .filter(
            or_(
                models.Course.title.ilike(f"%{query.rstrip()}%"),
                models.Section.crn == query.rstrip() if query.rstrip().isdigit() else False
            )
        )
        .all()
    )

    return results
