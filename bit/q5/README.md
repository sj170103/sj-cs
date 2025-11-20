# 과제 정리

##  프로젝트 구조
- `main.py`: FastAPI 엔드포인트. 질문/답변 API와 HTML 뷰 라우팅.
- `database.py`: SQLite 연결·세션 관리. `create_all()` 없이 Alembic 기반 운영.
- `models.py`: `Question`, `Answer` ORM 모델 정의 및 관계 설정.
- `domain/question`: 질문·답변 라우터와 Pydantic 스키마.
- `frontend`: 템플릿(`templates/`) + HTML 생성 모듈(`html_provider.py`).
- `migrations`: Alembic 설정 및 revision(`question`, `answer` 테이블 생성).

##  구현 내용
- FastAPI + SQLAlchemy로 질문/답변 CRUD API 구성.
- 질문 목록 HTML: 통계 카드, 접히는 질문 입력 폼, 답변 완료 뱃지, Bootstrap 기반 테이블.
- 질문 상세 HTML: 질문 메타, 답변 카드, 답변 등록 영역을 동일 테마로 구성.
- Alembic으로 스키마 버전 관리. `alembic upgrade head` 실행으로 DB 준비.

## 실행·검증 절차
1. 가상환경(예: `bit/q5/venv`) 활성화.
2. `alembic upgrade head` 실행 → `myapi.db`에 테이블 생성.
3. `uvicorn main:app --reload`로 서버 실행 후 `http://127.0.0.1:8000` 접속.
4. 질문 등록 → 목록/상세/답변 흐름 확인.
5. 보너스 과제 DB Browser for SQLite로 `myapi.db` 열어 `question`, `answer`, `alembic_version` 테이블을 확인.

