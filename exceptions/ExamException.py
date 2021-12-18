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


class CourseNotFound(ExamException):
    def __init__(self):
        super().__init__(status.HTTP_400_BAD_REQUEST,
                         "Course could not be found")


class ResolutionDoesNotExists(ExamException):
    def __init__(self):
        super().__init__(status.HTTP_404_NOT_FOUND,
                         "The resolution does not exist")


class InvalidStatusType(ExamException):
    def __init__(self, status_types):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            f"The status must be of one of the "
            f"following types: {', '.join(status_types)} ",
        )