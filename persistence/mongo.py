import os

import pymongo



class MongoDB:
    def __init__(self, db):
        self.db = db

    def saveExam(self, item: dict):
        key = {'id': item.get('id')}
        response = self.db.exams.update_one(key, {'$set': item}, upsert=True)
        return response.acknowledge

    def getExam(self, item: dict):
        return self.db.exams.find_one(item)

    def getExams(self, item: dict):
        return list(self.db.exams.find(item))

    def addResponse(self, item: dict):
        key = {'id': f'{item.get("user_id")}-{item.get("id")}'}
        response = self.db.responses.update_one(key, {'$set': item}, upsert=True)
        return response.acknowledge

    def getResponse(self, item: dict):
        return self.db.responses.find_one(item, upsert=True)

    def getResponses(self, item: dict):
        return list(self.db.exams.find(item))
