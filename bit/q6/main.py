# main.py
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse # HTML 응답을 위해 필요
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from domain.question import question_router, answer_router

# 우리가 만든 HTML 생성기 가져오기
from frontend import html_provider 

app = FastAPI()

app.include_router(question_router.router)
app.include_router(answer_router.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 화면(View) 엔드포인트 (API와 주소 구분) ---

@app.get("/", response_class=HTMLResponse)
def view_list(db: Session = Depends(get_db)):
    # 1. 데이터 가져오기
    questions = db.query(models.Question).order_by(models.Question.create_date.desc()).all()
    # 2. HTML 문자열로 변환해서 리턴
    return html_provider.get_list_html(questions)

@app.get("/view/detail/{question_id}", response_class=HTMLResponse)
def view_detail(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).get(question_id)
    return html_provider.get_detail_html(question)
