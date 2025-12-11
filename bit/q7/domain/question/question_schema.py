# domain/question/question_schema.py
import datetime
from pydantic import BaseModel

# 질문을 조회할 때 사용하는 규칙
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime

    class Config:
        from_attributes = True  # ORM 객체를 Pydantic 모델로 읽을 수 있게 설정

# 질문을 생성(저장)할 때 사용하는 규칙
class QuestionCreate(BaseModel):
    subject: str
    content: str