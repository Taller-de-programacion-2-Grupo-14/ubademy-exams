from pydantic import BaseModel, Field
from typing import List


class CreateExamSchema(BaseModel):
    id_course: int
    name: str = Field(min_length=10, max_length=255)
    questions: List[str] = []
    user_id: int


class EditExamSchema(BaseModel):
    id_course: int
    name: str = Field(min_length=10, max_length=255)
    questions: List[str] = []
    user_id: int


class GradeResolutionSchema(BaseModel):
    id_course: int
    id_exam: int
    id_student: int
    id_questions: List[str] = []
    corrections: str = Field(min_length=0, max_length=255)
    status: str = Field(min_length=8, max_length=11)
    user_id: int
    name: str


class InfoExamCompletitionSchema(BaseModel):
    course_id: int
    questions: List[str] = []
    answers: List[str] = []
    user_id: int
    name: str


class ExamPublishSchema(BaseModel):
    course_id: int
    user_id: int
    exam_name: str


class UserSchema(BaseModel):
    user_id: int
