# 📝 게시판 API 고도화 (Dependency Injection & Pydantic)

## 📌 과제 개요 (Project Overview)
이 프로젝트는 기존 FastAPI 게시판 API에 **의존성 주입(Dependency Injection)** 패턴과 **Pydantic 스키마**를 적용하여 안정성과 데이터 검증 기능을 강화한 버전입니다.
`contextlib`를 활용한 DB 세션 관리 자동화와 Pydantic을 이용한 입출력 데이터 검증을 구현했습니다.

---

## 📂 디렉터리 구조 (Directory Structure)

```text
bit/q7/
├── main.py                 # FastAPI 애플리케이션 진입점
├── database.py             # DB 연결 및 의존성 주입(get_db) 구현
├── domain/
│   └── question/
│       ├── question_router.py  # 의존성 주입 및 스키마 적용된 라우터
│       └── question_schema.py  # Pydantic 스키마 정의
└── ...
```

---

## 🛠 기술 스택 (Tech Stack)

| 구성 요소 | 사용 기술 |
|-----------|-----------|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Database | SQLite |

---

## 🚀 주요 구현 내용 (Implementation Details)

### 1. 의존성 주입 (Dependency Injection)
- **파일**: `database.py`
- **내용**: `contextlib.contextmanager`를 사용하여 `get_db` 제너레이터 함수를 구현.
- **효과**: API 요청 시 DB 세션을 자동으로 생성하고, 요청 처리가 끝나면 자동으로 닫아 리소스 누수를 방지함.

### 2. Pydantic 스키마 적용
- **파일**: `domain/question/question_schema.py`
- **내용**: `Question` 모델 정의 (`orm_mode=True` 설정).
- **효과**: API 응답 시 SQLAlchemy 모델 객체를 자동으로 JSON 호환 데이터로 변환 및 검증.

### 3. API 라우터 개선
- **파일**: `domain/question/question_router.py`
- **내용**: 
    - `Depends(get_db)`를 통해 DB 세션 주입.
    - `response_model`을 사용하여 응답 데이터 형식을 명시적으로 정의.

---

## ✅ 실행 및 테스트 (Execution & Testing)

### 1. 서버 실행
Swagger UI를 통해 직접 API를 테스트할 수 있습니다.

```bash
uvicorn main:app --reload
```
- 접속: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
