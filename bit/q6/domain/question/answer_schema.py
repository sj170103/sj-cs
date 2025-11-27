import datetime
from pydantic import BaseModel

class AnswerCreate(BaseModel):
    content: str

class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    question_id: int

    class Config:
        from_attributes = True