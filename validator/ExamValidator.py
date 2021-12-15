from external.courses import Courses


class ExamValidator:
    def __init__(self, database):
        self.db = database
        self.courses = Courses()

    def is_course_creator(self, course_id, user_id):
        course = self.courses.get_course(course_id, user_id)
        return course.get("can_edit")

    def exams_limit_reached(self, number, course_id, user_id):
        course = self.courses.get_course(course_id, user_id)
        original_quantity = course.get("exams", -1)
        return original_quantity <= number

    def is_student(self, course_id, user_id):
        course = self.courses.get_course(course_id, user_id)
        return course.get("is_subscribed")

    def is_course_collaborator(self, course_id, user_id):
        course = self.courses.get_course(course_id, user_id)
        return not course.get("can_collaborate", True)

    def is_grader(self, course_id, user_id):
        collab = self.is_course_collaborator(course_id, user_id)
        creator = self.is_course_creator(course_id, user_id)
        return collab or creator
