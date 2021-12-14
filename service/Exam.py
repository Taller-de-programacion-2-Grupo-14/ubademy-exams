# from requests import HTTPError
# from typing import List

from exceptions.ExamException import (
    IsNotTheCourseCreator,
    ExamDoesNotExist,
    ExamsLimitReached,
    InvalidUserAction,
    ExamAlreadyResolvedException
)
from validator.ExamValidator import ExamValidator
from persistence.local import DB


class ExamService:
    def __init__(self, database: DB):
        self.db = database
        self.validator = ExamValidator(database)

    def create_exam(self, create_exam_info, user_id):
        user_id = create_exam_info["user_id"]
        course_id = create_exam_info["id_course"]
        if not self.validator.is_course_creator(course_id, user_id):
            raise IsNotTheCourseCreator
        if self.validator.exams_limit_reached(course_id):
            raise ExamsLimitReached
        name = create_exam_info["name"]
        questions = create_exam_info["questions"]
        self.db.create_exam(name, questions)

    def edit_exam(self, edit_exam_data):
        course_id = edit_exam_data["id_course"]
        user_id = edit_exam_data["user_id"]
        exam_id = edit_exam_data["exam_id"]
        self._check_draft_exam_existance(course_id, exam_id)
        if not self.validator.is_course_creator(course_id, user_id):
            raise IsNotTheCourseCreator
        name = edit_exam_data["name"]
        questions = edit_exam_data["questions"]
        self.db.edit_exam(exam_id, course_id, name, questions)

    def publish_exam(self, publish_info):
        exam_id = publish_info["exam_id"]
        course_id = publish_info["course_id"]
        user_id = publish_info["user_id"]
        self._check_draft_exam_existance(course_id, exam_id)
        if not self.validator.is_course_creator(course_id, user_id):
            raise IsNotTheCourseCreator
        self.db.publish_exam(exam_id, course_id)

    def get_exams(self, course_id, user_id):
        grader = self.validator.is_grader(course_id, user_id)
        student = self.validator.is_student(course_id, user_id)
        if not grader and not student:
            raise InvalidUserAction
        exams = self.db.get_exams(course_id, user_id, grader)
        return exams

    def get_resolutions(self, course_id, user_id):
        grader = self.validator.is_grader(course_id, user_id)
        student = self.validator.is_student(course_id, user_id)
        if not grader and not student:
            raise InvalidUserAction
        exams = self.db.get_resolutions(course_id, user_id, grader)
        return exams

    def get_resolution(self, course_id, exam_id, student_id, user_id):
        self._check_published_exam_existance(course_id, exam_id)
        grader = self.validator.is_grader(course_id, user_id)
        student = self.validator.is_student(course_id, user_id)
        student = student and (user_id == student_id)
        if not grader or not student:
            raise InvalidUserAction
        exam_info = self.db.get_resolution(exam_id, student_id)
        return exam_info

    def grade_resolution(self, grade_resolution_data):
        id_exam = grade_resolution_data["exam_id"]
        id_student = grade_resolution_data["id_student"]
        corrections = grade_resolution_data["corrections"]
        status = grade_resolution_data["status"]
        course_id = grade_resolution_data["id_course"]
        user_id = grade_resolution_data["user_id"]
        self._check_published_exam_existance(course_id, id_exam)
        grader = self.validator.is_grader(course_id, user_id)
        student = self.validator.is_student(course_id, id_student)
        if not grader or not student:
            raise InvalidUserAction
        self.db.grade_exam(id_exam, id_student, corrections, status)

    def get_exam(self, course_id, exam_id, user_id):
        grader = self.validator.is_grader(course_id, user_id)
        student = self.validator.is_student(course_id, user_id)
        creator = self.validator.is_creator(course_id, user_id)
        if not grader or not student:
            raise InvalidUserAction
        exam = self.db.get_exam(course_id, exam_id, creator)
        if not exam:
            raise ExamDoesNotExist
        return exam

    def complete_exam(self, answers):
        id_exam = answers["id_exam"]
        answers = answers["answers"]
        user_id = answers["user_id"]
        course_id = answers["course_id"]
        self._check_published_exam_existance(course_id, id_exam)
        student = self.validator.is_student(course_id, user_id)
        if not student:
            raise InvalidUserAction
        if self.validator.resolution_exists(id_exam, user_id):
            raise ExamAlreadyResolvedException
        self.db.resolve_exam(answers, id_exam, user_id)

    def _check_draft_exam_existance(self, course_id, exam_id):
        drafts = self.db.get_course_drafts(course_id)
        if exam_id not in drafts:
            raise ExamDoesNotExist

    def _check_published_exam_existance(self, course_id, exam_id):
        published = self.db.get_course_published(course_id)
        if exam_id not in published:
            raise ExamDoesNotExist
