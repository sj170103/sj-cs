# todo.py
from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

import csv
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from model import TodoCreate, TodoItem

DATA_FILE = Path('todo_data.csv')
FIELDNAMES = ['id', 'title', 'done', 'created_at']

# 과제 요구: 전역 리스트 객체
todo_list: List[Dict[str, Any]] = []


def ensure_data_file() -> None:
    if not DATA_FILE.exists():
        with DATA_FILE.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_all_from_csv() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if not DATA_FILE.exists():
        return rows
    with DATA_FILE.open('r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                'id': int(r.get('id') or 0),
                'title': (r.get('title') or '').strip(),
                'done': (r.get('done') or '').strip().lower() in ('true', '1', 'yes'),
                'created_at': (r.get('created_at') or '').strip(),
            })
    return rows


def append_row_to_csv(row: Dict[str, Any]) -> None:
    with DATA_FILE.open('a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({
            'id': row['id'],
            'title': row['title'],
            'done': 'true' if row['done'] else 'false',
            'created_at': row['created_at'],
        })


def write_all_to_csv() -> None:
    # 전체 CSV 덮어쓰기: 업데이트/삭제 후에도 파일과 메모리가 동기화되도록 유지
    with DATA_FILE.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in todo_list:
            writer.writerow({
                'id': row['id'],
                'title': row['title'],
                'done': 'true' if row['done'] else 'false',
                'created_at': row['created_at'],
            })


def next_id() -> int:
    if not todo_list:
        return 1
    return max(item['id'] for item in todo_list) + 1


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 경고 없이 초기화: on_event(deprecated) 대신 lifespan 사용
    ensure_data_file()
    # CSV → 메모리 적재
    loaded = load_all_from_csv()
    todo_list.clear()
    todo_list.extend(loaded)
    yield


app = FastAPI(lifespan=lifespan)

router = APIRouter(prefix='/todos', tags=['todos'])


def get_todo_or_404(todo_id: int) -> Dict[str, Any]:
    # 공통 조회 유틸: 경로 매개변수 ID로 대상 Todo 검색
    for item in todo_list:
        if item['id'] == todo_id:
            return item
    raise HTTPException(status_code=404, detail={'warning': 'todo not found'})


@router.post('/add')
def add_todo(payload: TodoCreate) -> Dict[str, Any]:
    title = (payload.title or '').strip()
    if not title:
        raise HTTPException(status_code=400, detail={'warning': 'title is required'})

    item = {
        'id': next_id(),
        'title': title,
        'done': payload.done,
        'created_at': datetime.utcnow().isoformat(timespec='seconds') + 'Z',
    }
    # 메모리 & CSV 동시 반영
    todo_list.append(item)
    append_row_to_csv(item)

    return {
        'result': 'ok',
        'item': item,
    }


@router.get('/list')
def retrieve_todo() -> Dict[str, Any]:
    # 요구사항: Dict 타입으로 반환(리스트를 감싸서 반환)
    return {
        'items': todo_list,
        'count': len(todo_list),
    }


@router.get('/{todo_id}')
def get_single_todo(todo_id: int) -> Dict[str, Any]:
    item = get_todo_or_404(todo_id)
    return {'item': item}


@router.put('/{todo_id}')
def update_todo(todo_id: int, payload: TodoItem) -> Dict[str, Any]:
    item = get_todo_or_404(todo_id)
    # 기존 created_at 유지하면서 필드 갱신
    item['title'] = (payload.title or '').strip()
    if not item['title']:
        raise HTTPException(status_code=400, detail={'warning': 'title is required'})
    item['done'] = payload.done
    write_all_to_csv()
    return {
        'result': 'ok',
        'item': item,
    }


@router.delete('/{todo_id}')
def delete_single_todo(todo_id: int) -> Dict[str, Any]:
    item = get_todo_or_404(todo_id)
    todo_list.remove(item)
    write_all_to_csv()
    return {
        'result': 'ok',
        'deleted_id': todo_id,
    }


app.include_router(router)
app.mount('/client', StaticFiles(directory='client', html=True))


@app.get('/', include_in_schema=False)
def serve_client() -> RedirectResponse:
    # 루트 접근 시 정적 클라이언트 앱으로 안내
    return RedirectResponse(url='/client/')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('todo:app', host='127.0.0.1', port=8000, reload=True)
