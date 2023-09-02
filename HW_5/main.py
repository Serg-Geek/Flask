from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: bool

tasks = []

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
async def create_task(task: Task):
    tasks.append(task.dict())
    return {"message": "Task created successfully"}

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    for t in tasks:
        if t["id"] == task_id:
            t.update(task.dict())
            return {"message": "Task updated successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            tasks.remove(t)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")