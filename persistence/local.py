
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
        exam["status"] = ""
        self.db[table_id] = exam
        id_course_exams = f"course_{course_id}_exams"
        self.exam_courses_db[id_course_exams].append(id_exam)
        print(self.db)

    def get_draft_exams(self, course_id):
        print(self.exam_courses_db)
        print(self.db)
        exam_ids = self.exam_courses_db[f"course_{course_id}_exams"]
        results = []
        for exam_id in exam_ids:
            if self.db[f"exam_{exam_id}_item"]["status"] == "":
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
