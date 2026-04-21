from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date, time


class MeetingDayBase(BaseModel):
    day: str


class MeetingDayCreate(MeetingDayBase):
    pass


class MeetingDayRead(MeetingDayBase):
    meeting_id: int

    model_config = ConfigDict(from_attributes=True)


class InstructorBase(BaseModel):
    name: str


class InstructorCreate(InstructorBase):
    pass


class InstructorRead(InstructorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MeetingInstructorBase(BaseModel):
    instructor_id: int


class MeetingInstructorCreate(MeetingInstructorBase):
    pass


class MeetingInstructorRead(BaseModel):
    instructor: InstructorRead

    model_config = ConfigDict(from_attributes=True)


class MeetingBase(BaseModel):
    start_time: Optional[time] = None
    end_time: Optional[time] = None


class MeetingCreate(MeetingBase):
    meeting_days: List[MeetingDayCreate] = []
    instructor_ids: List[int] = []  # easier input API


class MeetingRead(MeetingBase):
    id: int
    section_crn: int
    meeting_days: List[MeetingDayRead] = []
    instructors: List[MeetingInstructorRead] = []

    model_config = ConfigDict(from_attributes=True)


class CourseBase(BaseModel):
    subject: str
    code: int
    title: str


class CourseCreate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: int
    sections: List["SectionRead"] = []

    model_config = ConfigDict(from_attributes=True)


class SemesterBase(BaseModel):
    name: str
    term: str
    year: int
    start_date: date
    end_date: date


class SemesterCreate(SemesterBase):
    pass


class SemesterRead(SemesterBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SectionBase(BaseModel):
    course_id: int
    semester_id: int


class SectionCreate(SectionBase):
    crn: int
    meetings: List[MeetingCreate] = []


class SectionRead(BaseModel):
    crn: int
    meetings: List[MeetingRead] = []

    model_config = ConfigDict(from_attributes=True)
