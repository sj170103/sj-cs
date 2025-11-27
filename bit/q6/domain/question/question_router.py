# domain/question/question_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Question
from domain.question import question_schema
import datetime

router = APIRouter(
    prefix="/api/question",
)

# 데이터베이스 세션을 생성하고 닫아주는 함수 (의존성 주입)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. 질문 목록 조회 API
@router.get("/list", response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    # 작성일시 역순(최신순)으로 조회
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return _question_list

# 2. 질문 등록 API
@router.post("/create")
def question_create(question: question_schema.QuestionCreate, db: Session = Depends(get_db)):
    # 질문 객체 생성
    db_question = Question(
        subject=question.subject,
        content=question.content,
        create_date=datetime.datetime.now()
    )
    db.add(db_question)
    db.commit() # 저장 확정
    return {"status": "success"}