from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db, engine

# Create database tables
models.course_models.Base.metadata.create_all(bind=engine)

app = FastAPI()