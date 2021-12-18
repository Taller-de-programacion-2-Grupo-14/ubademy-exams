import os
import requests


class Courses:
    def __init__(self):
        self.host = os.environ.get("COURSES_HOSTNAME")

    def get_course(self, course_id: int, user_id: int):
        url = f"{self.host}courses/{course_id}/view"
        response = requests.request(
            method="get",
            url=url,
            data={"user_id": user_id}
        )
        response.raise_for_status()
        return response.json()
