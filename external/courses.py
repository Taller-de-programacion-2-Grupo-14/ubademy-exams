import os
import requests


class Courses:
    def __init__(self):
        self.host = os.environ.get("COURSES_HOSTNAME")

    def get_course(self, course_id: int, user_id: int):
        url = f"{self.host}courses/exams"
        query_params = f"?user_id={user_id}&course_id={course_id}"
        response = requests.get(url + query_params)
        response.raise_for_status()
        return response.json()
