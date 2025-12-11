import datetime
from pydantic import BaseModel, field_validator

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

    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v