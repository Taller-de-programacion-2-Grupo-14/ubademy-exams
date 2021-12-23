import yaml
from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import pymongo
import os

import persistence.mongo
from controllers.Exam import ExamController
from exceptions.ExamException import ExamException
from schemas.Schemas import (
    CreateExamSchema,
    GradeResolutionSchema,
    UserSchema,
    InfoExamCompletitionSchema,
    ExamPublishSchema,
    EditExamSchema,
    GetResolution,
)
from service.Exam import ExamService
from validator.ExamValidator import ExamValidator
from queryparams.query_params import ExamQueryParams, ResolutionQueryParams


def get_client():
    env = os.getenv("ENVIROMENT")
    env = env if env else "test"
    url = f"mongodb+srv://ubademy:{os.getenv('UBADEMY_PASSWORD')}@cluster0"
    client = pymongo.MongoClient(
        url + ".39prr.mongodb.net/exams?retryWrites=true&w=majority"
    )
    return client[env]


db = persistence.mongo.MongoDB(get_client())
app = FastAPI()
exam_service = ExamService(db, ExamValidator(db))
exam_controller = ExamController(exam_service)


@app.post("/exams/create")
def create_exam(create_exam_data: CreateExamSchema):
    return exam_controller.handle_create_exam(create_exam_data.dict())


@app.put("/exams/edit")
def edit_exam(edit_exam_data: EditExamSchema):
    return exam_controller.handle_edit_exam(edit_exam_data.dict())


@app.post("/exams/publish")
def publish_exam(publish_info: ExamPublishSchema):
    return exam_controller.handle_publish_exam(publish_info.dict())


@app.get("/exams/{course_id}")
def get_exams(
    course_id: int, user: UserSchema, filter: ExamQueryParams = Depends(ExamQueryParams)
):
    return exam_controller.handle_get_exams(course_id, user.user_id, filter.get_data())


@app.get("/resolutions/{course_id}")
def get_resolutions(
    course_id: int,
    user: UserSchema,
    filter: ResolutionQueryParams = Depends(ResolutionQueryParams),
):
    return exam_controller.handle_get_resolutions(
        course_id, user.user_id, filter.get_status()
    )


@app.get("/resolution/{course_id}/{student_id}")
def get_resolution(course_id: int, student_id: int, body: GetResolution):
    return exam_controller.handle_get_resolution(
        course_id, student_id, body.user_id, body.exam_name
    )


@app.patch("/resolution/grade/{course_id}/{student_id}")
def grade_resolution(course_id: int, grade_resolution_inf: GradeResolutionSchema):
    return exam_controller.handle_grade_resolution(
        course_id, grade_resolution_inf.dict()
    )


@app.get("/exam/{course_id}/{exam_name}")
def get_exam(course_id: int, exam_name: str, user: UserSchema):
    return exam_controller.handle_get_exam(course_id, exam_name, user.user_id)


@app.post("/exams/resolve/{course_id}")
def resolve_exam(course_id: int, answers: InfoExamCompletitionSchema):
    return exam_controller.handle_resolve_exam(course_id, answers.dict())


@app.get("/doc-yml")
def get_swagger():
    with open("docs/swagger.yaml") as f:
        swagger = yaml.safe_load(f)
        return swagger


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    fields = []
    for err in errors:
        value = {
            "field": err.get("loc", ["invalid field"])[-1],
            "message": err.get("msg", ""),
        }
        fields.append(value)
    final_status = status.HTTP_400_BAD_REQUEST
    return JSONResponse(
        status_code=final_status,
        content=jsonable_encoder({"errors": fields, "status": final_status}),
    )


@app.exception_handler(ExamException)
def handle_course_exception(request: Request, exc: ExamException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"message": exc.message, "status": exc.status_code}),
    )


@app.exception_handler(Exception)
def handleUnknownException(request: Request, exc: Exception):
    error = f"{type(exc).__name__}"
    msg = f"{exc.args[0]}"
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=jsonable_encoder(
            {
                "message": f"Unknown error: {error} with message: {msg}",
                "status": status.HTTP_503_SERVICE_UNAVAILABLE,
            }
        ),
    )
