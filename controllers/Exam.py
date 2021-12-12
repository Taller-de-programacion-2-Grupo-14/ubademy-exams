from fastapi import status
from service.Exam import ExamService


class ExamController:
    def __init__(self, exam_service: ExamService):
        self.service = exam_service

    def handle_get_exams(self, course_id):
        exams = self.service.get_exams(course_id)
        return self._get_list_response(exams)

    def handle_create_exam(self, create_exam_info, user_id):
        self.service.create_exam(create_exam_info, user_id)
        return {"message": "Exam created successfully",
                "status": status.HTTP_200_OK}

    def handle_edit_exam(self, exam_id, edit_exam_data, user_id):
        self.service.edit_exam(exam_id, edit_exam_data, user_id)
        return {"message": "Exam edited successfully",
                "status": status.HTTP_200_OK}

    def handle_publish_exam(self, publish_info, user_id):
        exam_id = publish_info["exam_id"]
        course_id = publish_info["course_id"]
        self.service.publish_exam(exam_id, user_id, course_id)
        return {"message": "Exam published successfully",
                "status": status.HTTP_200_OK}

    def handle_get_exam_correct(self, exam_id, student_id):
        exam_info = self.service.get_exam_correct(exam_id, student_id)
        return self._get_list_response(exam_info)

    def handle_correct_exam(self, correct_exam_data):
        self.service.correct_exam(correct_exam_data)
        return {"message": "Exam created successfully",
                "status": status.HTTP_200_OK}

    def handle_get_my_exams(self, course_id, user_id):
        exams = self.service.get_my_exams(course_id, user_id)
        return self._get_list_response(exams)

    def handle_get_todo_exam(self, exam_id, user_id):
        exam_info = self.service.get_todo_exam(exam_id, user_id)
        return {"message": exam_info, "status": status.HTTP_200_OK}

    def complete_exam(self, answers, user_id):
        self.service.complete_exam(answers, user_id)
        return {"message": "Exam completed successfully",
                "status": status.HTTP_200_OK}

    def _get_list_response(self, array):
        return {"message": array, "status": self._get_list_status(array)}

    def _get_list_status(self, array):
        return status.HTTP_200_OK if len(array) else status.HTTP_204_NO_CONTENT
