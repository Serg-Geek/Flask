# Создать API для управления списком задач. Каждая задача должна содержать поля "название", "описание" и "статус"
# (выполнена/не выполнена). API должен позволять выполнять CRUD операции с задачами.

from typing import List
import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

DATABASE_URL = "sqlite:///seminar_db2.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(32)),
    sqlalchemy.Column("description", sqlalchemy.String(128)),
    sqlalchemy.Column("status", sqlalchemy.Boolean()),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

app = FastAPI()


class TaskIn(BaseModel):
    title: str = Field(max_length=32, title="Title")
    description: str = Field(max_length=128, title="Description")
    status: bool = Field(default=False, title="Status")


class Task(TaskIn):
    id: int


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/tasks/', response_model=List[Task])
async def read_tasks():
    query = tasks.select()
    return await database.fetch_all(query)


@app.get('/tasks/{task_id}', response_model=Task)
async def read_task(task_id: int):
    query = tasks.select().where(tasks.c.id == task_id)
    return await database.fetch_one(query)


@app.post('/tasks/', response_model=Task)
async def create_task(task: TaskIn):
    query = tasks.insert().values(**task.dict())
    last_record_id = await database.execute(query)
    return {**task.dict(), "id": last_record_id}


@app.put('/tasks/{task_id}', response_model=Task)
async def update_task(new_task: TaskIn, task_id: int):
    query = tasks.update().where(tasks.c.id == task_id).values(**new_task.dict())
    await database.execute(query)
    return {**new_task.dict(), "id": task_id}


@app.delete('/tasks/{task_id}')
async def delete_task(task_id: int):
    query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(query)
    return {"message": "Task deleted"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000)