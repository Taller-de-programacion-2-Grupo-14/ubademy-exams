from collections import defaultdict


class DB:
    def __init__(self):
        self.db = {}
        self.answers_db = {}
        self.exam_courses_db = defaultdict(list)
        self.id = 1

    def get_exams(self, course_id):
        print(self.exam_courses_db)
        print(self.db)
        exam_ids = self.exam_courses_db[f"course_{course_id}_exams"]
        results = []
        for exam_id in exam_ids:
            if self.db[f"exam_{exam_id}_item"]["status"] == "":
                answer = self.answers_db.get(f"exam_{exam_id}", "")
                if not answer:
                    return results
                title = self.db[f"exam_{exam_id}_item"]["title"]
                qs = self.db[f"exam_{exam_id}_item"]["questions"]
                r = {}
                r["exam_name"] = title
                r["id_student"] = answer["id_student"]
                r["questions"] = qs
                id_qs = []
                i = 1
                for x in qs:
                    id = f"q{i}e{exam_id}"
                    id_qs.append(id)
                    i += 1
                r["id_questions"] = id_qs
                r["answers"] = answer["answers"]
                results.append(r)
        return results

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

    def get_course_drafts(self, course_id):
        table_id = f"course_{course_id}_exams_draft"
        return self.exam_courses_db.get(table_id, [])

    def get_draft_exams(self, course_id):
        exam_ids = self.exam_courses_db[f"course_{course_id}_exams"]
        results = []
        for exam_id in exam_ids:
            if self.db[f"exam_{exam_id}_item"]["status"] == "draft":
                title = self.db[f"exam_{exam_id}_item"]["title"]
                qs = self.db[f"exam_{exam_id}_item"]["questions"]
                r = {}
                r["exam_name"] = title
                r["questions"] = qs
                id_qs = []
                i = 1
                for x in qs:
                    id = f"q{i}e{exam_id}"
                    id_qs.append(id)
                    i += 1
                r["id_questions"] = id_qs
                results.append(r)
        return results

    def get_exam_info_correction(self, exam_id, student_id):
        info_exam = self.db.get(f"exam_{exam_id}_item", "")
        answer = self._get_student_answer(student_id, exam_id)
        if not answer:
            return {}
        result = {}
        course_id = self._get_course_id(exam_id)
        result["id_course"] = course_id
        result["id_exam"] = exam_id
        result["id_student"] = answer.get("id_student", "")
        result["questions"] = info_exam.get("questions", "")
        result["answers"] = answer.get("answers", "")
        result["status"] = answer.get("status", "")
        # se puede sacar el id_questions
        id_questions = []
        for i in range(1, len(info_exam.get("questions", ""))+1):
            id_questions.append(f"q_{i}e{exam_id}")
        result["id_questions"] = id_questions
        return result

    def correct_exam(self, id_exam, id_student, corrections, status):
        answer, pos = self._get_student_answer(id_student, id_exam)
        if not answer:
            return {}
        self.answers_db[pos]["corrections"] = corrections
        self.answers_db[pos]["status"] = status

    def get_my_exams(self, course_id, user_id):
        key_course = f"course_{course_id}_exams"
        exam_ids = self.exam_courses_db.get(key_course, "")
        if not exam_ids:
            return []
        undonde_exams = []
        for exam_id in exam_ids:
            answer, _ = self._get_student_answer(user_id, exam_id)
            if not answer:
                undonde_exams.append(exam_id)
        if not undonde_exams:
            return []
        exams_list = []
        for exam_id in undonde_exams:
            result = {}
            title = self.db[f"exam_{exam_id}_item"].get("title", "")
            qs = self.db[f"exam_{exam_id}_item"].get("questions", "")
            course_id = self._get_course_id(exam_id)
            result["name"] = title
            result["id_exam"] = exam_id
            result["id_course"] = course_id
            result["questions"] = qs
            exams_list.append(result)
        return exams_list

    def get_todo_exam(self, exam_id, user_id):
        exam = self.db.get(f"exam_{exam_id}_item", "")
        if not exam:
            return {}
        name = exam.get("title", "")
        questions = exam.get("questions", "")
        exam_info = {}
        exam_info["name"] = name
        exam_info["id_exam"] = exam_id
        exam_info["questions"] = questions
        return exam_info

    def complete_exam(self, answers, id_exam, user_id):
        new_entry = {}
        new_entry["id_student"] = user_id
        new_entry["answers"] = answers
        # esto supongo en realidad q podria agregarse al momento d corregir..?
        new_entry["corrections"] = ""
        new_entry["status"] = "not corrected"
        table_id = f"exam_{id_exam}"
        if table_id in self.answers_db:
            self.answers_db[table_id].append(new_entry)
        else:
            self.answers_db[table_id] = [new_entry]

    def _get_student_answer(self, student_id, exam_id):
        answers = self.answers_db.get(f"exam_{exam_id}", "")
        if not answers:
            return {}
        for a in answers:
            if a.get("id_student", "") == student_id:
                return a, answers.index(a)
        return {}, None

    def _get_course_id(self, exam_id):
        course_id = ""
        for key, value in self.exam_courses_db.items():
            if exam_id in value:
                course_id = key
        return course_id if course_id else None
