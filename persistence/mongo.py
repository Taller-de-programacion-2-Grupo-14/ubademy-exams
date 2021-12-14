def _getExamKey(name, courseId):
    return {'title': name, 'course': courseId}


def _getKeyResolution(name, userId, courseId):
    key = {}
    if name:
        key.update({'exam': name})
    if userId:
        key.update({'user': userId})
    if courseId:
        key.update({'course': courseId})
    return key


class MongoDB:
    def __init__(self, db):
        self.db = db

    def createExam(self, name: str, courseId, questions: dict):
        key = _getExamKey(name, courseId)
        item = {'status': 'drafted'}
        item.update({'questions': questions})
        response = self.db.exams.update_one(key, {'$set': questions}, upsert=True)
        return response.acknowledge

    def editExam(self, courseId, name, questions):
        key = _getExamKey(name, courseId)
        response = self.db.exams.update_one(key, {'$set': {'questions': questions}}, upsert=True)
        return response.acknowledge

    def getExam(self, name, courseId):
        return self.db.exams.find_one(_getExamKey(name, courseId))

    def getExams(self, name, courseId):
        item = {}
        if name:
            item.update({'name': name})
        if courseId:
            item.update({'course': courseId})
        return list(self.db.exams.find(item))

    def publishExam(self, name, courseId):
        key = _getExamKey(name, courseId)
        response = self.db.exams.update_one(key, {'$set': {'status': 'published'}}, upsert=True)
        return response.acknowledge

    def addResolution(self, userId, examName, courseId, item: dict):
        key = _getKeyResolution(examName, userId, courseId)
        response = self.db.responses.update_one(key, {'$set': {'answer': item}}, upsert=True)
        return response.acknowledge

    def getResolution(self, name, userId, courseId):
        key = _getKeyResolution(name, userId, courseId)
        return self.db.responses.find_one(key, upsert=True)

    def getResponses(self, name, userId, courseId):
        key = _getKeyResolution(name, userId, courseId)
        return list(self.db.exams.find(key))

    def gradeExam(self, name, userId, courseId, corrections: dict, status):
        if not (name and userId and courseId):
            raise Exception
        correction = {'correction': corrections, 'status': status}
        response = self.db.responses.update_one(_getKeyResolution(name, userId, courseId), {'$set': correction})
        return response.acknowledge
