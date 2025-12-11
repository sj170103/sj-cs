from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Question
from domain.question import question_schema
import datetime

router = APIRouter(
    prefix="/api/question",
)

# 1. 질문 목록 조회 API
@router.get("/list", response_model=list[question_schema.Question])
def question_list(db=Depends(get_db)):
    with db as session:
        # 작성일시 역순(최신순)으로 조회
        _question_list = session.query(Question).order_by(Question.create_date.desc()).all()
        return _question_list

# 2. 질문 등록 API
@router.post("/create")
def question_create(question: question_schema.QuestionCreate, db=Depends(get_db)):
    try:
        with db as session:
            # 질문 객체 생성
            db_question = Question(
                subject=question.subject,
                content=question.content,
                create_date=datetime.datetime.now()
            )
            session.add(db_question)
            session.commit() # 저장 확정
            return {"status": "success"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e