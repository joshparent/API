from sqlalchemy import Column, ForeignKey, Integer, Text, Date, UniqueConstraint, Time, CHAR, CheckConstraint
from sqlalchemy.orm import relationship
from ..database import Base


class Semester(Base):
    __tablename__ = 'semesters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    term = Column(Text, nullable=False)
    year = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    __table_args__ = (
        UniqueConstraint("term", "year", name="unique_term_year"),
    )

    sections = relationship("Section", back_populates="semester")


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    subject = Column(Text, nullable=False)
    code = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("subject", "code", name="unique_subject_code"),
    )

    sections = relationship("Section", back_populates="course")


class Section(Base):
    __tablename__ = 'sections'

    crn = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    semester_id = Column(Integer, ForeignKey('semesters.id'), nullable=False)

    meetings = relationship("Meeting", back_populates="section", cascade="all, delete-orphan", passive_deletes=True)
    semester = relationship("Semester", back_populates="sections")
    course = relationship("Course", back_populates="sections")


class Meeting(Base):
    __tablename__ = 'meetings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    section_crn = Column(Integer, ForeignKey('sections.crn', ondelete="CASCADE"), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    section = relationship("Section", back_populates="meetings")

    meeting_days = relationship("MeetingDay", back_populates="meeting", cascade="all, delete-orphan")

    instructors = relationship("MeetingInstructor", back_populates="meeting", cascade="all, delete-orphan")


class MeetingDay(Base):
    __tablename__ = 'meeting_days'

    meeting_id = Column(Integer, ForeignKey('meetings.id', ondelete="CASCADE"), primary_key=True)
    day = Column(CHAR(1), primary_key=True)

    __table_args__ = (CheckConstraint("day IN ('M','T','W','R','F','S','U')", name='valid_day_check'),)

    meeting = relationship("Meeting", back_populates="meeting_days", passive_deletes=True)


class Instructor(Base):
    __tablename__ = 'instructors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)

    meetings = relationship("MeetingInstructor", back_populates="instructor", cascade="all, delete-orphan")


class MeetingInstructor(Base):
    __tablename__ = 'meeting_instructors'

    meeting_id = Column(Integer, ForeignKey('meetings.id', ondelete="CASCADE"), primary_key=True)
    instructor_id = Column(Integer, ForeignKey('instructors.id'), primary_key=True)

    meeting = relationship("Meeting", back_populates="instructors")
    instructor = relationship("Instructor", back_populates="meetings")
