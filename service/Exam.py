from exceptions.ExamException import (
    IsNotTheCourseCreator,
    ExamDoesNotExist,
    ExamsLimitReached,
    InvalidUserAction,
    ExamAlreadyResolvedException, ResolutionDoesNotExists
)
from validator.ExamValidator import ExamValidator
from persistence.mongo import MongoDB


class ExamService:
    def __init__(self, database: MongoDB):
        self.db = database
        self.validator = ExamValidator(database)

    def create_exam(self, create_exam_info):
        user_id = create_exam_info["user_id"]
        course_id = create_exam_info["id_course"]
        if not self.validator.is_course_creator(course_id, user_id):
            raise IsNotTheCourseCreator
        exams = len(self.db.get_exams(course_id, False))
        if self.validator.exams_limit_reached(exams, course_id, user_id):
            raise ExamsLimitReached
        name = create_exam_info["name"]
        questions = create_exam_info["questions"]
        self.db.create_exam(name, course_id, questions)

    def edit_exam(self, edit_exam_data):
        course_id = edit_exam_data["id_course"]
        user_id = edit_exam_data["user_id"]
        name = edit_exam_data["name"]
        self._check_draft_exam_existance(course_id, name)
        if not self.validator.is_course_creator(course_id, user_id):
            raise IsNotTheCourseCreator
        questions = edit_exam_data["questions"]
        self.db.edit_exam(course_id, name, questions)

    def publish_exam(self, publish_info):
        name = publish_info["exam_name"]
        course_id = publish_info["course_id"]
        user_id = publish_info["user_id"]
        if not self.validator.is_course_creator(course_id, user_id):
            raise IsNotTheCourseCreator
        self._check_draft_exam_existance(course_id, name)
        exams = len(self.db.get_exams(course_id, False))
        if self.validator.exams_limit_reached(exams, course_id, user_id):
            raise ExamsLimitReached
        self.db.publish_exam(name, course_id)

    def get_exams(self, course_id, user_id, filters):
        creator = self.validator.is_course_creator(course_id, user_id)
        student = self.validator.is_student(course_id, user_id)
        collaborator = self.validator.is_course_collaborator(course_id,
                                                             user_id)
        name = filters.get("name")
        status = filters.get("status")
        if not creator and not student and not collaborator:
            raise InvalidUserAction
        if student:
            exams = self.get_undone_exams(user_id, course_id)
        if collaborator:
            exams = self.db.get_course_status(course_id, "published")
        if creator:
            if name:
                exams = [self.db.get_exam(name, course_id, creator)]
            else:
                exams = self.db.get_exams(course_id, creator)
            if status:
                status = status.lower()
                exams = [e for e in exams if e.get("status") == status]
        return exams

    def get_resolutions(self, course_id, user_id):
        grader = self.validator.is_grader(course_id, user_id)
        student = self.validator.is_student(course_id, user_id)
        if not grader and not student:
            raise InvalidUserAction
        resolutions = self.db.get_responses(None, user_id, course_id, grader)
        exams = self.db.get_exams(course_id, False)
        for r in resolutions:
            for exam in exams:
                if r.get("exam") == exam.get("title"):
                    r["questions"] = exam["questions"]
        return resolutions

    def get_resolution(self, course_id, name, student_id, user_id):
        self._check_published_exam_existance(course_id, name)
        grader = self.validator.is_grader(course_id, user_id)
        is_student = self.validator.is_student(course_id, user_id)
        student = (user_id == student_id) and is_student
        if not grader and not student:
            raise InvalidUserAction
        exam_info = self.db.get_resolution(name, student_id, course_id)
        return exam_info

    def grade_resolution(self, course_id, grade_resolution_data):
        id_student = grade_resolution_data["id_student"]
        corrections = grade_resolution_data["corrections"]
        status = grade_resolution_data["status"]
        user_id = grade_resolution_data["user_id"]
        name = grade_resolution_data["name"]
        grader = self.validator.is_grader(course_id, user_id)
        if not grader:
            raise InvalidUserAction
        self._check_resolution_exam(course_id, name, id_student)
        self.db.grade_exam(name, id_student, course_id, corrections, status)
        resolutions = self.get_resolutions(course_id, user_id)
        self.validator.notify_course(course_id, user_id, resolutions)

    def get_exam(self, course_id, exam_name, user_id):
        student = self.validator.is_student(course_id, user_id)
        creator = self.validator.is_course_creator(course_id, user_id)
        if not creator and not student:
            raise InvalidUserAction
        exam = self.db.get_exam(exam_name, course_id, creator)
        if not exam:
            raise ExamDoesNotExist
        return exam

    def complete_exam(self, course_id, resolution):
        answers = resolution["answers"]
        user_id = resolution["user_id"]
        name = resolution['name']
        self._check_published_exam_existance(course_id, name)
        student = self.validator.is_student(course_id, user_id)
        if not student:
            raise InvalidUserAction
        if self.db.get_resolution(name, user_id, course_id):
            raise ExamAlreadyResolvedException
        self.db.add_resolution(user_id, name, course_id, answers)

    def _check_draft_exam_existance(self, course_id, name):
        drafts = self.db.get_course_status(course_id, "draft")
        existance = False
        for exam in drafts:
            if exam.get("title") == name:
                existance = True
                break
        if not existance:
            raise ExamDoesNotExist

    def _check_published_exam_existance(self, course_id, name):
        published = self.db.get_course_status(course_id, "published")
        existance = False
        for exam in published:
            if exam["title"] == name:
                existance = True
                break
        if not existance:
            raise ExamDoesNotExist

    def get_undone_exams(self, user_id, course_id):
        course_exams = self.db.get_exams(course_id, False)
        user_done = self.db.get_resolutions(user_id, course_id)
        exams, done = [], set()
        for v in user_done:
            done.add(v.get('exam'))
        for v in course_exams:
            title = v.get('title')
            if title and title not in done:
                exams.append(v)
        return exams

    def _check_resolution_exam(self, course_id, name, user_id):
        if not self.db.get_resolution(name, user_id, course_id):
            raise ResolutionDoesNotExists
