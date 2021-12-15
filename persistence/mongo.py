def _get_exam_key(name, course_id):
    return {'title': name, 'course': course_id}


def _get_key_resolution(name, user_id, course_id):
    key = {}
    if name:
        key.update({'exam': name})
    if user_id:
        key.update({'user': user_id})
    if course_id:
        key.update({'course': course_id})
    return key


class MongoDB:
    def __init__(self, db):
        self.db = db

    def create_exam(self, name: str, course_id, questions: dict):
        key = _get_exam_key(name, course_id)
        item = {'status': 'draft'}
        item.update({'questions': questions})
        response = self.db.exams.update_one(key, {'$set': item}, upsert=True)
        return response.acknowledged

    def edit_exam(self, course_id, name, questions):
        key = _get_exam_key(name, course_id)
        response = self.db.exams.update_one(key,
                                            {'$set': {'questions': questions,
                                             'name': name}}, upsert=True)
        return response.acknowledged

    def get_exam(self, name, course_id, creator):
        exam_key = _get_exam_key(name, course_id)
        if not creator:
            exam_key.update({'status': 'published'})
        return self.db.exams.find_one(exam_key, {'_id': 0})

    def get_exams(self, course_id, creator):
        item = {}
        if course_id:
            item.update({'course': course_id})
        if not creator:
            item.update({'status': 'published'})
        exams = list(self.db.exams.find(item, {'_id': 0}))
        return exams

    def publish_exam(self, name, course_id):
        key = _get_exam_key(name, course_id)
        response = self.db.exams.update_one(key,
                                            {'$set': {'status': 'published'}},
                                            upsert=True)
        return response.acknowledged

    def add_resolution(self, user_id, exam_name, course_id, item: dict):
        key = _get_key_resolution(exam_name, user_id, course_id)
        response = self.db.responses.update_one(
                                                key,
                                                {'$set':
                                                    {'answer': item,
                                                        "status": "nc"}},
                                                upsert=True)
        return response.acknowledged

    def get_resolution(self, name, user_id, course_id):
        key = _get_key_resolution(name, user_id, course_id)
        return self.db.responses.find_one(key, {'_id': 0})

    def get_responses(self, name, user_id, course_id, grader):
        key = _get_key_resolution(name=name, user_id="", course_id=course_id)
        if not grader:
            key.update({'user_id': user_id})
        return list(self.db.exams.find(key))

    def grade_exam(self, name, user_id, course_id, corrections, status):
        if not (name and user_id and course_id):
            raise Exception
        correction = {'correction': corrections, 'status': status}
        response = self.db.responses.update_one(_get_key_resolution(name, user_id, course_id),
                                                {'$set': correction})
        return response.acknowledged

    def get_course_status(self, course_id, status):
        key = {"course_id": course_id, 'status': status}
        return list(self.db.exams.find(key, {'_id': 0}))

    def get_resolutions(self, user_id, course_id):
        key = _get_key_resolution(None, user_id, course_id)
        return list(self.db.responses.find(key, {'_id': 0}))
