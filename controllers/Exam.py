from fastapi import status
from service.Exam import ExamService


class ExamController:
    def __init__(self, exam_service: ExamService):
        self.service = exam_service

    def handle_get_exams(self, course_id):
        exams = self.service.get_exams(course_id)
        return self._get_list_response(exams)

    def handle_create_exam(self, create_exam_info):
        self.service.create_exam(create_exam_info)
        return {"message": "Exam created successfully",
                "status": status.HTTP_200_OK}

    def handle_get_draft_exams(self, course_id):
        exams = self.service.get_draft_exams(course_id)
        return self._get_list_response(exams)

    def _get_list_response(self, array):
        return {"message": array, "status": self._get_list_status(array)}

    def _get_list_status(self, array):
        return status.HTTP_200_OK if len(array) else status.HTTP_204_NO_CONTENT
