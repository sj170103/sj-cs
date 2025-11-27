# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
    # 답변들과 연결 (Question.answers로 답변 목록을 가져올 수 있음)
    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
    # 질문 id와 연결 (어떤 질문의 답변인지 표시)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", back_populates="answers")