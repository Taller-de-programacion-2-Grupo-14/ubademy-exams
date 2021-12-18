from collections import defaultdict


class DB:
    def __init__(self):
        self.db = {}
        self.answers_db = {}
        self.exam_courses_db = defaultdict(list)
        self.id = 1

    def create_exam(self, course_id, name, questions):
        id_exam = self.id + 1
        table_id = f"exam_{id_exam}_item"
        exam = {}
        exam["title"] = name
        exam["questions"] = questions
        exam["id"] = id_exam
        exam["status"] = "draft"
        self.db[table_id] = exam
        id_course_exams = f"course_{course_id}_exams_draft"
        self.exam_courses_db[id_course_exams].append(id_exam)

    def edit_exam(self, exam_id, name, questions):
        table_id = f"exam_{exam_id}_item"
        self.db[table_id]["title"] = name
        self.db[table_id]["questions"] = questions

    def publish_exam(self, exam_id, course_id):
        table_id = f"course_{course_id}_exams_draft"
        new_id = f"course_{course_id}_exams_published"
        self.exam_courses_db[table_id].remove(exam_id)
        if new_id in self.exam_courses_db:
            self.exam_courses_db[new_id].append(exam_id)
        else:
            self.exam_courses_db[new_id] = [exam_id]
        self.db[f"exam_{exam_id}_item"]["status"] = "published"

    def get_exams(self, course_id, user_id, grader):
        ids_published = self.exam_courses_db[f"course_{course_id}_exams_published"]
        exam_ids = []
        if grader:
            ids_draft = self.exam_courses_db[f"course_{course_id}_exams_draft"]
            exam_ids = ids_published + ids_draft
        else:
            for exam_id in ids_published:
                if user_id not in self.answers_db[f"exam_{exam_id}"]:
                    exam_ids.append(exam_id)
        results = []
        for exam_id in exam_ids:
            for exam in self.db[f"exam_{exam_id}_item"]:
                exam_name = exam["title"]
                questions = exam["questions"]
                status = exam["status"]
                r = {}
                r["exam_name"] = exam_name
                r["questions"] = questions
                r["status"] = status
                r["exam_id"] = exam_id
                results.append(r)
        return results

    def get_resolutions(self, course_id, user_id, grader):
        exam_ids = self.exam_courses_db[f"course_{course_id}_exams_published"]
        if not exam_ids:
            return []
        resolutions = []
        if grader:
            for exam_id in exam_ids:
                exam = self.db[f"exam_{exam_id}_item"]
                users = self.answers_db[f"exam_{exam_id}"]
                if not users:
                    continue
                for user in users:
                    resolution = self.answers_db[f"exam_{exam_id}_{user}"]
                    r = {}
                    r["id_student"] = user
                    r["exam_id"] = exam_id
                    r["exam_name"] = exam["title"]
                    r["questions"] = exam["questions"]
                    r["answers"] = resolution["answers"]
                    r["status"] = resolution["status"]
                    r["correction"] = resolution["corrections"]
                    resolutions.append(r)
        else:
            for exam_id in exam_ids:
                if user_id in self.answers_db[f"exam_{exam_id}"]:
                    exam = self.db[f"exam_{exam_id}_item"]
                    resolution = self.answers_db[f"exam_{exam_id}_{user_id}"]
                    r = {}
                    r["id_student"] = user_id
                    r["exam_id"] = exam_id
                    r["exam_name"] = exam["title"]
                    r["questions"] = exam["questions"]
                    r["answers"] = resolution["answers"]
                    r["status"] = resolution["status"]
                    r["correction"] = resolution["corrections"]
                    resolutions.append(r)
        return resolutions

    def get_resolution(self, exam_id, student_id):
        if f"exam_{exam_id}" not in self.answers_db:
            return {}
        if student_id not in self.answers_db[f"exam_{exam_id}"]:
            return {}
        exam = self.db.get(f"exam_{exam_id}_item")
        resolution = self.answers_db[f"exam_{exam_id}_{student_id}"]
        result = {}
        course_id = self._get_course_id(exam_id)
        result["id_course"] = course_id
        result["id_exam"] = exam_id
        result["id_student"] = student_id
        result["questions"] = exam["questions"]
        result["answers"] = resolution["answers"]
        result["status"] = resolution["status"]
        return result

    def grade_exam(self, id_exam, id_student, corrections, status):
        if f"exam_{id_exam}" not in self.answers_db:
            return {}
        if id_student not in self.answers_db[f"exam_{id_exam}"]:
            return {}
        self.answers_db[f"exam_{id_exam}_{id_student}"]["corrections"] = corrections
        self.answers_db[f"exam_{id_exam}_{id_student}"]["status"] = status

    def get_exam(self, course_id, exam_id, creator):
        table_id = "exam_{exam_id}_items"
        if creator:
            drafts = self.get_course_drafts(course_id, exam_id)
            if exam_id in drafts:
                exam = self.db[table_id]
                name = exam["title"]
                questions = exam["questions"]
                r = {}
                r["name"] = name
                r["id_exam"] = exam_id
                r["questions"] = questions
                return r
        published = self.get_course_published(course_id, exam_id)
        if exam_id not in published:
            return {}
        exam = self.db[table_id]
        name = exam["title"]
        questions = exam["questions"]
        r = {}
        r["name"] = name
        r["id_exam"] = exam_id
        r["questions"] = questions
        return r

    def resolve_exam(self, answers, id_exam, user_id):
        new_entry = {}
        new_entry["id_student"] = user_id
        new_entry["answers"] = answers
        new_entry["corrections"] = ""
        new_entry["status"] = "nc"
        if f"exam_{id_exam}" in self.answers_db:
            self.answers_db[f"exam_{id_exam}"].append(user_id)
        else:
            self.answers_db[f"exam_{id_exam}"] = [user_id]
        self.answers_db[f"exam_{id_exam}_{user_id}"] = new_entry

    def get_exam_resoltions(self, exam_id):
        if f"exam_{exam_id}" in self.answers_db:
            return self.answers_db[f"exam_{exam_id}"]
        return []

    def _get_course_id(self, exam_id):
        course_id = ""
        for key, value in self.exam_courses_db.items():
            if exam_id in value:
                course_id = key
        return course_id if course_id else None

    def get_course_drafts(self, course_id):
        table_id = f"course_{course_id}_exams_draft"
        return self.exam_courses_db.get(table_id, [])

    def get_course_published(self, course_id):
        table_id = f"course_{course_id}_exams_published"
        return self.exam_courses_db.get(table_id, [])
