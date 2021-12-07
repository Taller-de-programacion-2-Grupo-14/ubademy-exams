import uvicorn  # ToDo Before merge delete this
# from fastapi import FastAPI, Request, status, Depends
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from schemas.Schemas import CreateExamSchema
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


# @app.get("/exams/correct/{exam_id}")
# def get_exam_correct():
#     return


# @app.patch("/exams/correct/{exam_id}")
# def correct_exam(correct_exam_data: InfoExamCorrectedSchema):
#     return


# @app.get("/exams/view/{course_id}")
# def view_my_exams():
#     return


# @app.post("/exams/complete/{course_id}")
# def get_exam():
#     return


# @app.post("/exams/complete/{course_id}")
# def complete_exam():
#     return


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
