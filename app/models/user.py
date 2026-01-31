from pydantic import BaseModel


class delete_user_schema(BaseModel):
    user_id: str
    email: str


class update_user_schema(delete_user_schema):
    name: str


class catagory_schema(BaseModel):
    catagory: str
    color: str


class add_catagory_schema(BaseModel):
    user_id: str
    catagory_data: catagory_schema


class update_catagory_schema(BaseModel):
    user_id: str
    catagory_data: list[catagory_schema]


class delete_todo_schema(BaseModel):
    user_id: str
    todo_id: str


class new_todo_schema(BaseModel):
    title: str
    desc: str
    due_date: str
    priority: int
    catagory: str
    status: int
    user_id: str


class update_todo_schema(new_todo_schema):
    todo_id: str


class update_todo_status_schema(BaseModel):
    todo_id: str
    user_id: str
    status: int
