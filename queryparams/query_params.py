from fastapi import Query
from typing import Optional


class ExamQueryParams:
    def __init__(
        self, name: Optional[str] = Query(None), status: Optional[str] = Query(None)
    ):
        self.data = {"name": name, "status": status}

    def get_data(self):
        return self.data


class ResolutionQueryParams:
    def __init__(self, status: Optional[str] = Query(None)):
        self.data = {"status": status}

    def get_status(self):
        return self.data.get("status")
