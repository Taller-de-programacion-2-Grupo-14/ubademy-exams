from fastapi import status
from service.Exam import ExamService


class ExamController:
    def __init__(self, exam_service: ExamService):
        self.service = exam_service

    def handle_create_exam(self, create_exam_info):
        self.service.create_exam(create_exam_info)
        return {"message": "Exam created successfully",
                "status": status.HTTP_200_OK}

    def handle_edit_exam(self, edit_exam_data):
        self.service.edit_exam(edit_exam_data)
        return {"message": "Exam edited successfully",
                "status": status.HTTP_200_OK}

    def handle_publish_exam(self, publish_info):
        self.service.publish_exam(publish_info)
        return {"message": "Exam published successfully",
                "status": status.HTTP_200_OK}

    def handle_get_exams(self, course_id, user_id, filters):
        exams = self.service.get_exams(course_id, user_id, filters)
        return self._get_list_response(exams)

    def handle_get_resolutions(self, course_id, user_id):
        resolutions = self.service.get_resolutions(course_id, user_id)
        return self._get_list_response(resolutions)

    def handle_get_resolution(self, course_id, student_id, user_id, name):
        exam_info = self.service.get_resolution(course_id, name,
                                                student_id, user_id)
        return exam_info if exam_info is not None else {}

    def handle_grade_resolution(self, course_id, grade_resolution_data):
        self.service.grade_resolution(course_id, grade_resolution_data)
        return {"message": "Exam created successfully",
                "status": status.HTTP_200_OK}

    def handle_get_exam(self, course_id, exam_name, user_id):
        exam = self.service.get_exam(course_id, exam_name, user_id)
        return {"message": exam, "status": status.HTTP_200_OK}

    def handle_resolve_exam(self, course_id, answers):
        self.service.complete_exam(course_id, answers)
        return {"message": "Exam completed successfully",
                "status": status.HTTP_200_OK}

    def _get_list_response(self, array):
        return {"message": array, "status": self._get_list_status(array)}

    def _get_list_status(self, array):
        return status.HTTP_200_OK if len(array) else status.HTTP_204_NO_CONTENT
