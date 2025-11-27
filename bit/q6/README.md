# 과제 정리

## 과제 요구 (q6.md)
- `domain/question/question_router.py`를 APIRouter로 생성하고 `prefix='/api/question'`을 설정한다.
- SQLite 데이터를 SQLAlchemy ORM으로 조회하는 `question_list()` GET 엔드포인트를 만든다.
- 라우터를 `main.py`에 `include_router()`로 등록해 앱에 연결한다.
- Python 표준 패키지 외 의존성 추가 없이 PEP 8, 문자열/들여쓰기 규칙을 따른다.

## 구현 내용
- `domain/question/question_router.py`: `APIRouter(prefix='/api/question')` 구성, `@router.get('/list', response_model=list[question_schema.Question])`에서 ORM으로 질문을 생성일 내림차순 조회해 반환. DB 세션 의존성은 `SessionLocal`로 관리. `@router.post('/create')`로 질문 등록도 제공.
- `main.py`: 질문/답변 라우터를 `include_router()`로 등록해 API 경로를 활성화. HTML 뷰 라우팅은 기존대로 `frontend` 모듈의 HTML을 반환.
- `database.py`, `models.py`: SQLite 연결과 `Question`, `Answer` ORM 모델을 사용해 라우터가 DB를 조회·저장하도록 유지.

## 검증 방법
1. 가상환경 활성화(예: `bit/q5/venv`).
2. 필요 시 `alembic upgrade head`로 `myapi.db`를 준비(이미 생성돼 있으면 생략).
3. 서버 실행: `uvicorn main:app --reload`.
4. `http://127.0.0.1:8000/docs` 접속 → `GET /api/question/list`를 실행해 ORM 기반 목록이 반환되는지 확인. 필요하면 `POST /api/question/create`로 질문을 추가하고 다시 목록을 조회해 반영 여부를 확인.
5. HTML 확인: `http://127.0.0.1:8000/`에서 목록 페이지, `http://127.0.0.1:8000/view/detail/{id}`에서 상세 페이지가 정상 표시되는지 본다.
6. (선택) DB Browser for SQLite로 `myapi.db`를 열어 `question`, `answer`, `alembic_version` 테이블 상태를 확인.
