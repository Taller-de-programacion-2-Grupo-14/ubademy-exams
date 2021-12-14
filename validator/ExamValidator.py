from persistence.local import DB


class ExamValidator:
    def __init__(self, database: DB):
        self.db = database

    def is_course_creator(self, course_id, user_id):
        is_creator = True
        return is_creator

    def exams_limit_reached(self, course_id):
        return False

    def is_student(self, course_id, user_id):
        return True

    def is_course_collaborator(self, course_id, user_id):
        return True

    def is_grader(self, course_id, user_id):
        collab = self.is_course_collaborator(course_id, user_id)
        creator = self.is_course_creator(course_id, user_id)
        return collab or creator

    def resolution_exists(self, id_exam, user_id):
        resolutions = self.db.get_exam_resoltions(id_exam)
        return user_id in resolutions
