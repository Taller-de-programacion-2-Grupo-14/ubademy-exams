# from requests import HTTPError
# from typing import List

# from exceptions.CourseException import *
from persistence.local import DB
# from validator.CourseValidator import CourseValidator


class ExamService:
    def __init__(self, database: DB):
        self.db = database

    def get_exams(self, course_id):
        exams = self.db.get_exams(course_id)
        return exams

    def create_exam(self, create_exam_info):
        course_id = create_exam_info.get("id_course", "")
        name = create_exam_info.get("name", "")
        questions = create_exam_info.get("questions", "")
        self.db.create_exam(course_id, name, questions)

    def get_draft_exams(self, course_id):
        exams = self.db.get_draft_exams(course_id)
        return exams
