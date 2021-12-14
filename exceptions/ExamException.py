from fastapi import status


class ExamException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class IsNotTheCourseCreator(ExamException):
    def __init__(self):
        super().__init__(status.HTTP_403_FORBIDDEN,
                         "The user is not the course creator")


class ExamDoesNotExist(ExamException):
    def __init__(self):
        super().__init__(status.HTTP_404_NOT_FOUND,
                         "The exam does not exist")


class ExamsLimitReached(ExamException):
    def __init__(self):
        super().__init__(status.HTTP_409_CONFLICT,
                         "Exams quantity limit reached")


class InvalidUserAction(ExamException):
    def __init__(self):
        super().__init__(status.HTTP_403_FORBIDDEN,
                         "Invalid User action")


class ExamAlreadyResolvedException(ExamException):
    def __init__(self):
        super().__init__(status.HTTP_403_FORBIDDEN,
                         "Exam already resolved by user")
