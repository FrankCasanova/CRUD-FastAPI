from typing import List
from fastapi import FastAPI, HTTPException

#schemas
from schemas import Task, TaskWithID

#operations
from operations import create_task, delete_task, get_all_tasks, get_task_by_id, modify_task


app = FastAPI(
    title="Tasks API",
    description="An API for managing your tasks",
    version="0.1.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "John Doe",
        "url": "https://example.com/contact",
        "email": "kxu2H@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://example.com/license",
    },
)

@app.get("/")
async def root():
    return {"message": "Task Application"}

@app.get("/tasks", response_model=List[TaskWithID])
async def get_tasks():
    return get_all_tasks()

@app.get("/tasks/{task_id}", response_model=TaskWithID)
async def get_task(task_id: int):
    return get_task_by_id(task_id)

@app.post("/tasks", response_model=TaskWithID)
async def create_task_endpoint(task: Task):
    return create_task(task)

@app.put("/tasks/{task_id}", response_model=TaskWithID)
async def update_task_endpoint(task_id: int, task: Task):
    return modify_task(task_id, task)

@app.delete("/tasks/{task_id}", response_model=TaskWithID)
async def delete_task_endpoint(task_id: int):
    return delete_task(task_id)




