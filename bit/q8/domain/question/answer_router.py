from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Question, Answer
# 같은 폴더(domain.question)에 있는 스키마를 가져오도록 수정
from domain.question import answer_schema 

router = APIRouter(
    prefix='/api/answer',
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/create/{question_id}')
def answer_create(question_id: int,
                  _answer_create: answer_schema.AnswerCreate,
                  db: Session = Depends(get_db)):
    
    question = db.query(Question).get(question_id)
    if not question:
        raise HTTPException(status_code=404, detail='Question not found')
    
    db_answer = Answer(question=question,
                       content=_answer_create.content,
                       create_date=datetime.now())
    db.add(db_answer)
    db.commit()
    
    return {'status': 'success'}