from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
    done: bool = False


class TodoCreate(TodoBase):
    # POST /todos/add 입력을 검증
    pass


class TodoItem(TodoBase):
    # 요구사항: 수정 기능을 위한 모델(BaseModel 상속)
    pass
