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
    try:
        return get_all_tasks()
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

@app.get("/task/{task_id}", response_model=TaskWithID)
async def get_task(task_id: int):
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/task", response_model=TaskWithID)
async def create_task_endpoint(task: Task):
    return create_task(task)

@app.put("/task/{task_id}", response_model=TaskWithID)
async def update_task_endpoint(task_id: int, task: Task):
    task = modify_task(task_id, task)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/task/{task_id}", response_model=TaskWithID)
async def delete_task_endpoint(task_id: int):
    task = delete_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, reload_delay=1)
