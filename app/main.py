from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, joinedload
from . import schemas
from .models import course_models as models
from .database import get_db, engine
from sqlalchemy import or_, distinct
from fastapi.middleware.cors import CORSMiddleware

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize API
app = FastAPI()

# App middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


# Retrieves all semesters
@app.get("/semesters", response_model=list[schemas.SemesterRead])
def get_semesters(db: Session = Depends(get_db)):
    return db.query(models.Semester).all()


# Retrieves all courses for a specific semester
@app.get("/semesters/{semester_id}/courses", response_model=list[schemas.CourseRead])
def get_courses_by_semester(semester_id: int, db: Session = Depends(get_db)):
    courses = (
        db.query(models.Course)
        .join(models.Section)
        .filter(models.Section.semester_id == semester_id)
        .distinct()
        .all()
    )

    return courses


# Retrieves all subjects for a specific semester
@app.get("/semesters/{semester_id}/subjects", response_model=list[str])
def get_subjects_by_semester(semester_id: int, db: Session = Depends(get_db)):
    subjects = (
        db.query(distinct(models.Course.subject))
        .join(models.Section, models.Section.course_id == models.Course.id)
        .filter(models.Section.semester_id == semester_id)
        .all()
    )

    return [s[0] for s in subjects]


# Retrieves all courses that match a crn or title query for a given semester
@app.get("/semesters/{semester_id}/courses/search", response_model=list[schemas.SectionRead])
def search_courses(semester_id: int, query: str, db: Session = Depends(get_db)):
    query = query.strip()
    filters = [models.Course.title.ilike(f"%{query}%")]

    if query.isdigit():
        filters.append(models.Course.id == int(query))

    results = (
        db.query(models.Section)
        .join(models.Course)
        .options(joinedload(models.Section.course),
                 joinedload(models.Section.semester),
                 joinedload(models.Section.meetings).joinedload(models.Meeting.instructors).joinedload(
                     models.MeetingInstructor.instructor),
                 joinedload(models.Section.meetings).joinedload(models.Meeting.meeting_days), )
        .filter(models.Section.semester_id == semester_id, or_(*filters))
        .all()
    )

    return results
