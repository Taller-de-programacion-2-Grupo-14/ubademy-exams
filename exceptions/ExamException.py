# from fastapi import status


class ExamException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
