import uvicorn
# from fastapi import FastAPI, Request, status
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
# import yaml
from fastapi import FastAPI
from schemas.Schemas import (
    CreateExamSchema,
    InfoExamCorrectedSchema,
    UserSchema,
    InfoExamCompletitionSchema,
    ExamPublishSchema
)
from service.Exam import ExamService
from controllers.Exam import ExamController
from persistence.local import DB
# from exceptions.ExamException import ExamException

app = FastAPI()
exam_service = ExamService(DB())
exam_controller = ExamController(exam_service)


@app.post("/exams/create")
def create_exam(create_exam_data: CreateExamSchema, user: UserSchema):
    return exam_controller.handle_create_exam(create_exam_data.dict(),
                                              user.user_id)


@app.put("/exams/edit/{exam_id}")
def edit_exam(exam_id, edit_exam_data: CreateExamSchema, user: UserSchema):
    return exam_controller.handle_edit_exam(exam_id, edit_exam_data.dict(),
                                            user.user_id)


@app.post("/exams/publish")
def publish_exam(publish_info: ExamPublishSchema, user: UserSchema):
    return exam_controller.handle_publish_exam(publish_info,
                                               user.user_id)


@app.get("/exams/{course_id}")
def get_exams(course_id: int, user: UserSchema):
    return exam_controller.handle_get_exams(course_id)


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


@app.post("/exams/complete/{exam_id}")
def complete_exam(answers: InfoExamCompletitionSchema, user: UserSchema):
    return exam_controller.complete_exam(answers, user.user_id)


# @app.get("/doc-yml")
# def get_swagger():
#     with open("docs/swagger.yaml") as f:
#         swagger = yaml.safe_load(f)
#         return swagger


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     response = await call_next(request)
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     response.headers["Access-Control-Allow-Headers"] = "*"
#     response.headers["Access-Control-Allow-Methods"] = "*"
#     return response


# @app.exception_handler(RequestValidationError)
# def validation_exception_handler(request: Request,
#                                  exc: RequestValidationError):
#     errors = exc.errors()
#     fields = []
#     for err in errors:
#         value = {
#             "field": err.get("loc", ["invalid field"])[-1],
#             "message": err.get("msg", ""),
#         }
#         fields.append(value)
#     final_status = status.HTTP_400_BAD_REQUEST
#     return JSONResponse(
#         status_code=final_status,
#         content=jsonable_encoder({"errors": fields, "status": final_status}),
#     )


# @app.exception_handler(ExamException)
# def handle_course_exception(request: Request, exc: ExamException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content=jsonable_encoder({"message": exc.message,
#                                   "status": exc.status_code}),
#     )


# @app.exception_handler(Exception)
# def handleUnknownException(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#         content=jsonable_encoder(
#             {
#                 "message":
#                 f"Unknown error: {type(exc).__name__} with message: \
#                     {exc.args[0]}",
#                 "status": status.HTTP_503_SERVICE_UNAVAILABLE,
#             }
#         ),
#     )


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
