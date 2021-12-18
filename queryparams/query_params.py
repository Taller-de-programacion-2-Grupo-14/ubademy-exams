from fastapi import Query
from typing import Optional


class ExamQueryParams:
    def __init__(self, name: Optional[str] = Query(None)):
        self.name = name
