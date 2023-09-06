# Создать API для управления списком задач. Приложение должно иметь возможность создавать, обновлять, удалять и получать список задач.
# ● Создайте модуль приложения и настройте сервер и маршрутизацию.
# ● Создайте класс Task с полями id, title, description и status.
# ● Создайте список tasks для хранения задач.
# ● Создайте маршрут для получения списка задач (метод GET).
# ● Создайте маршрут для создания новой задачи (метод POST).
# ● Создайте маршрут для обновления задачи (метод PUT).
# ● Создайте маршрут для удаления задачи (метод DELETE).
# ● Реализуйте валидацию данных запроса и ответа.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

TASKS = []


class Task(BaseModel):
    id_: int
    title: str
    description: str
    status: str


@app.get('/tasks/')
async def all_tasks():
    return {'tasks': TASKS}


@app.post('/tasks/add')
async def add_task(task: Task):
    TASKS.append(task)
    return {"task": task, "status": "added"}


@app.put('/tasks/update/{task_id}')
async def update_task(task_id: int, task: Task):
    for t in TASKS:
        if t.id_ == task_id:
            t.title = task.title
            t.description = task.description
            t.status = task.status
            return {"task": task, "status": "updated"}
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete('/tasks/delete/{task_id}')
async def delete_task(task_id: int):
    for t in TASKS:
        if t.id_ == task_id:
            TASKS.remove(t)
            return {"status": "success"}
    raise HTTPException(status_code=404, detail="Task not found")

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
#
# app = FastAPI()
#
# TASKS = []
#
#
# class Task(BaseModel):
#     id_: int
#     title: str
#     description: str
#     status: str
#
#
# @app.get('/tasks/')
# async def all_tasks():
#     return {'tasks': TASKS}
#
#
# @app.post('/task/add')
# async def add_task(task: Task):
#     TASKS.append(task)
#     return {"task": task, "status": "added"}
#
#
# @app.put('/task/update/{task_id}')
# async def update_task(task_id: int, task: Task):
#     for t in TASKS:
#         if t.id_ == task_id:
#             t.title = task.title
#             t.description = task.description
#             t.status = task.status
#         return {"task": task, "status": "updated"}
#     return HTTPException(404, 'Task not found')
#
#
# @app.delete('/task/delete/{task_id}')
# async def delete_task(task_id: int):
#     for t in TASKS:
#         if t.id_ == task_id:
#             TASKS.remove(t)
#         return {"status": "success"}
#     return HTTPException(404, 'Task not found')