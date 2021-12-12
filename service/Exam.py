# from requests import HTTPError
# from typing import List

from exceptions.ExamException import (
    IsNotTheCourseCreator,
    ExamDoesNotExist
)


class ExamService:
    def __init__(self, database):
        self.db = database

    def get_exams(self, course_id):
        exams = self.db.get_exams(course_id)
        return exams

    def create_exam(self, create_exam_info, user_id):
        course_id = create_exam_info.get("id_course")
        self._is_course_creator_validation(course_id, user_id)
        name = create_exam_info.get("name")
        questions = create_exam_info.get("questions")
        self.db.create_exam(name, questions)

    def edit_exam(self, exam_id, edit_exam_data, user_id):
        course_id = edit_exam_data.get("id_course")
        self._is_course_creator_validation(course_id, user_id)
        exam_ids = self.db.get_course_drafts(course_id)
        if exam_id not in exam_ids or not self.db.get_exam_or_none(exam_id):
            raise ExamDoesNotExist
        name = edit_exam_data.get("name")
        questions = edit_exam_data.get("questions")
        self.db.edit_exam(exam_id, course_id, name, questions)

    def publish_exam(self, exam_id, user_id, course_id):
        self._is_course_creator_validation(course_id, user_id)
        exam_ids = self.db.get_course_drafts(course_id)
        if exam_id not in exam_ids or not self.db.get_exam_or_none(exam_id):
            raise ExamDoesNotExist
        self.db.publish_exam(exam_id, course_id)

    def get_exam_correct(self, exam_id, student_id):
        exam_info = self.db.get_exam_info_correction(exam_id, student_id)
        return exam_info

    def correct_exam(self, correct_exam_data):
        id_exam = correct_exam_data.get("exam_id")
        id_student = correct_exam_data.get("id_student")
        corrections = correct_exam_data.get("corrections")
        status = correct_exam_data.get("status")
        self.db.correct_exam(id_exam, id_student, corrections, status)

    def get_my_exams(self, course_id, user_id):
        exams = self.db.get_my_exams(course_id, user_id)
        return exams

    def get_todo_exam(self, exam_id, user_id):
        exam_info = self.db.get_todo_exam(exam_id, user_id)
        return exam_info

    def complete_exam(self, answers, user_id):
        id_exam = answers.get("id_exam")
        answers = answers.get("answers")
        self.db.complete_exam(answers, id_exam, user_id)

    def _is_course_creator_validation(self, course_id, user_id):
        is_creator = True
        if not is_creator:
            raise IsNotTheCourseCreator
