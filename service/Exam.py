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

class ExamService:
    def __init__(self, database):
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
        self.db.createExam(name, course_id, questions)

    def edit_exam(self, edit_exam_data):
        course_id = edit_exam_data["id_course"]
        user_id = edit_exam_data["user_id"]
        exam_id = edit_exam_data["exam_id"]
        name = edit_exam_data["name"]
        self._check_draft_exam_existance(course_id, name)
        if not self.validator.is_course_creator(course_id, user_id):
            raise IsNotTheCourseCreator
        questions = edit_exam_data["questions"]
        self.db.editExam(course_id, name, questions)

    def publish_exam(self, publish_info):
        name = publish_info["exam_name"]
        course_id = publish_info["course_id"]
        user_id = publish_info["user_id"]
        self._check_draft_exam_existance(course_id, name)
        if not self.validator.is_course_creator(course_id, user_id):
            raise IsNotTheCourseCreator
        self.db.publishExam(name, course_id)

    def get_exams(self, course_id, user_id): #No entiendo que quiere hacer este endpoint
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
        exams = self.db.getResponses(None, course_id, user_id)
        return exams

    def get_resolution(self, course_id, exam_id, student_id, user_id):
        self._check_published_exam_existance(course_id, exam_id)
        grader = self.validator.is_grader(course_id, user_id)
        student = self.validator.is_student(course_id, user_id)
        student = student and (user_id == student_id)
        if not grader or not student:
            raise InvalidUserAction
        exam_info = self.db.getResolution(exam_id, student_id, course_id)
        return exam_info

    def grade_resolution(self, grade_resolution_data):
        id_exam = grade_resolution_data["exam_id"]
        id_student = grade_resolution_data["id_student"]
        corrections = grade_resolution_data["corrections"]
        status = grade_resolution_data["status"]
        course_id = grade_resolution_data["id_course"]
        user_id = grade_resolution_data["user_id"]
        name = grade_resolution_data['name']
        self._check_published_exam_existance(course_id, name)
        grader = self.validator.is_grader(course_id, user_id)
        student = self.validator.is_student(course_id, id_student)
        if not grader or not student:
            raise InvalidUserAction
        self.db.gradeExam(name, id_student, course_id, corrections, status)

    def get_exam(self, course_id, exam_id, user_id):
        grader = self.validator.is_grader(course_id, user_id)
        student = self.validator.is_student(course_id, user_id)
        creator = self.validator.is_creator(course_id, user_id)
        if not grader or not student:
            raise InvalidUserAction
        exam = self.db.getExam(exam_id, course_id)
        if not exam:
            raise ExamDoesNotExist
        return exam

    def complete_exam(self, answers):
        id_exam = answers["id_exam"]
        answers = answers["answers"]
        user_id = answers["user_id"]
        course_id = answers["course_id"]
        name = answers['name']
        self._check_published_exam_existance(course_id, name)
        student = self.validator.is_student(course_id, user_id)
        if not student:
            raise InvalidUserAction
        #if self.validator.resolution_exists(id_exam, user_id):
        #    raise ExamAlreadyResolvedException
        self.db.addResolution(user_id, name, course_id, answers)

    def _check_draft_exam_existance(self, course_id, name):
        draft = self.db.getExam(name, course_id)
        if bool(draft):
            raise ExamDoesNotExist

    def _check_published_exam_existance(self, course_id, exam_id):
        published = self.db.getExam(course_id, exam_id)
        if exam_id not in published:
            raise ExamDoesNotExist
