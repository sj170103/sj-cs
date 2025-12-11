# 📝 게시판 API 고도화 (질문 등록 & 프론트엔드)

## 📌 과제 개요 (Project Overview)
이 프로젝트는 게시판 서비스의 핵심 기능인 **질문 등록** 기능을 구현하고, 이를 테스트할 수 있는 **프론트엔드 페이지**를 추가한 버전입니다.
Pydantic의 유효성 검사 기능을 활용하여 빈 제목이나 내용을 방지하고, 사용자 친화적인 웹 인터페이스를 제공합니다.

---

## 📂 디렉터리 구조 (Directory Structure)

```text
bit/q8/
├── main.py                 # FastAPI 앱 및 화면 라우터(View)
├── domain/
│   └── question/
│       ├── question_router.py  # 질문 등록 API (POST)
│       └── question_schema.py  # 입력 데이터 유효성 검사 (Validator)
├── frontend/
│   └── templates/
│       └── create_question.html # 질문 등록 폼 (HTML)
└── ...
```

---

## 🛠 기술 스택 (Tech Stack)

| 구성 요소 | 사용 기술 |
|-----------|-----------|
| Framework | FastAPI |
| Validation | Pydantic (Field Validator) |
| Template Engine | Jinja2 |
| Frontend | HTML, CSS |

---

## 🚀 주요 구현 내용 (Implementation Details)

### 1. 스키마 유효성 검사 (Schema Validation)
- **파일**: `domain/question/question_schema.py`
- **내용**: `field_validator`를 사용하여 `subject`와 `content` 필드의 공백 여부를 검사.
- **효과**: 빈 문자열이나 공백만 있는 데이터가 DB에 저장되는 것을 원천 차단하여 데이터 무결성 보장.

### 2. 질문 등록 API
- **파일**: `domain/question/question_router.py`
- **내용**: 
    - `POST /api/question/create` 엔드포인트 구현.
    - `Depends(get_db)`를 통해 트랜잭션 안전성을 보장하며 데이터 저장.

### 3. 프론트엔드 구현 (Bonus)
- **파일**: `frontend/templates/create_question.html`, `main.py`
- **내용**: 
    - 사용자 입력을 받을 수 있는 HTML 폼 작성.
    - `main.py`에 `/view/create` 경로를 추가하여 HTML 렌더링.

---

## ✅ 실행 및 테스트 (Execution & Testing)

### 1. 서버 실행
서버를 실행하여 API와 프론트엔드 페이지를 모두 사용할 수 있습니다.

```bash
uvicorn main:app --reload
```

### 2. 기능 확인
- **질문 등록 페이지**: [http://127.0.0.1:8000/view/create](http://127.0.0.1:8000/view/create) 접속하여 질문 등록 시도.
- **API 문서**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)에서 `POST /api/question/create` 테스트.
