import uvicorn  # ToDo Before merge delete this
# from fastapi import FastAPI, Request, status, Depends
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from schemas.Schemas import (
    CreateExamSchema,
    InfoExamCorrectedSchema,
    UserSchema,
    InfoExamCompletitionSchema
)
from service.Exam import ExamService
from controllers.Exam import ExamController
from persistence.local import DB

app = FastAPI()
exam_service = ExamService(DB())
exam_controller = ExamController(exam_service)


@app.get("/exams/{course_id}")
def get_exams(course_id: int):
    return exam_controller.handle_get_exams(course_id)


@app.patch("/exams/create")
def create_exam(create_exam_data: CreateExamSchema):
    return exam_controller.handle_create_exam(create_exam_data.dict())


@app.get("/exams/drafts/{course_id}")
def get_draft_exams(course_id: int):
    return exam_controller.handle_get_draft_exams(course_id)


@app.get("/exams/correct/{exam_id}/{student_id}")
def get_exam_correct(exam_id: int, student_id: int):
    return exam_controller.handle_get_exam_correct(exam_id, student_id)


@app.patch("/exams/correct/{exam_id}")
def correct_exam(correct_exam_data: InfoExamCorrectedSchema):
    return exam_controller.handle_correct_exam(correct_exam_data.dict())


@app.get("/exams/view/{course_id}")
def view_my_exams(course_id: int, user: UserSchema):
    return exam_controller.handle_get_my_exams(course_id, user.user_id)


@app.get("/exams/complete/{exam_id}")
def get_exam(exam_id: int, user: UserSchema):
    return exam_controller.handle_get_todo_exam(exam_id, user.user_id)


@app.post("/exams/complete/{course_id}")
def complete_exam(answers: InfoExamCompletitionSchema, user: UserSchema):
    return exam_controller.complete_exam(answers, user.user_id)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
