# Todo 서비스 Q3 구현 요약

## 1. 개발 환경 준비
- Python 3.12 기반, `python3-venv`와 `pip` 설치가 필요합니다 (WSL에서 `sudo apt install python3-venv python3-pip`).
- 프로젝트 루트(`/mnt/c/cs/sj-cs/bit/q3`)에 가상환경 생성 후 필요한 패키지를 설치합니다.
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install fastapi uvicorn
  ```
- 서버 실행: `uvicorn todo:app --reload --host 127.0.0.1 --port 8000`

## 2. 기능 구현 요약
- **모델**: `model.py`에 `TodoCreate`, `TodoItem` Pydantic 모델을 정의해 POST/PUT 요청의 유효성 검사와 스키마 일관성을 확보했습니다.
- **CSV 저장소**: `todo.py`에서 CSV 파일(`todo_data.csv`)을 생성/로드/추가/전체 덮어쓰기 하는 헬퍼를 만들고, 앱 lifespan 단계에서 메모리와 동기화합니다.
- **REST API**: `/todos` 라우터에 다음 엔드포인트를 구현했습니다.
  - `POST /todos/add`: Todo 추가
  - `GET /todos/list`: 전체 목록 조회
  - `GET /todos/{id}`: 단일 조회
  - `PUT /todos/{id}`: 제목/완료 상태 수정
  - `DELETE /todos/{id}`: 삭제
- **정적 클라이언트**: `/client` 경로로 `frontend/index.html`을 서빙하고, 루트 접근 시 SPA로 리다이렉트합니다. 순수 JS로 API를 호출해 목록/추가/조회/수정/삭제를 수행할 수 있습니다.

## 3. 검증 절차
1. FastAPI 서버 실행 (`uvicorn todo:app --reload`).
2. 브라우저에서 `http://127.0.0.1:8000/client/` 접속해 추가/조회/수정/삭제 흐름을 확인합니다.
3. 명세 요구대로 `curl`로도 검증합니다.
   ```bash
   curl -s -X POST http://127.0.0.1:8000/todos/add -H 'Content-Type: application/json' -d '{"title":"Read specs","done":false}'
   curl -s http://127.0.0.1:8000/todos/1
   curl -s -X PUT http://127.0.0.1:8000/todos/1 -H 'Content-Type: application/json' -d '{"title":"Review specs","done":true}'
   curl -s -X DELETE http://127.0.0.1:8000/todos/1
   ```

## 4. 디렉터리 구조
```
bit/q3/
├── todo.py          # FastAPI 애플리케이션, CSV 헬퍼, REST 라우터, 정적 서빙
├── model.py         # TodoCreate/TodoItem Pydantic 모델
├── client/
│   └── index.html   # 순수 JS 기반 Todo 클라이언트 SPA
├── todo_data.csv    # CSV 저장소
└── README.md        # 현재 문서
```

