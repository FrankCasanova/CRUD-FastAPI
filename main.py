from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

#schemas
from schemas import Task, TaskWithID, taskv2WithID, UserInDB, User

#operations
from operations import create_task, delete_task, get_all_tasks, get_task_by_id, modify_task, read_all_tasks_v2

#security
from security import fakely_hash_password, fake_token_generator, get_user_from_token, fake_users_db


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


#-----------Authentication----------------
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Generate a token for the given username and password.

    Args:
    form_data: OAuth2PasswordRequestForm containing the username and password.

    Returns:
    A dict with the access token and the token type.
    """
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    user = UserInDB(**user_dict)
    hashed_password = fakely_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    token = fake_token_generator(user)
    return {"access_token": token, "token_type": "bearer"}
    
#-----------------------------------------
#-----------Users------------------------
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_user_from_token)):
    """
    Get the current user.

    Returns:
    The current user.
    """
    return current_user
#-----------------------------------------


@app.get("/")
async def root():
    return {"message": "Task Application"}

#-----------V2----------------
@app.get("/v2/tasks", response_model=List[taskv2WithID])
async def get_tasks_v2():
    """
    Get all tasks from the database.

    Returns:
    A list of all tasks in the database.
    """
    return read_all_tasks_v2()

@app.get("/tasks", response_model=List[TaskWithID])
async def get_tasks(
    status: Optional[str] = None,
    title: Optional[str] = None
):
    
    """
    Get all tasks from the database, filtered by status and title.

    Args:
        status (Optional[str]): The status of the tasks to filter by.
        title (Optional[str]): The title of the tasks to filter by.

    Returns:
        List[TaskWithID]: A list of all tasks in the database, filtered by status and title.

    Raises:
        HTTPException: If something goes wrong while getting the tasks from the database.
    """
    try:
        tasks = get_all_tasks()
        if status is not None:
            tasks = [task for task in tasks if task.status.lower() == status.lower()]
        if title is not None:
            tasks = [task for task in tasks if task.title.lower() == title.lower()]
        return tasks
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

@app.get("/tasks/search", response_model=List[TaskWithID])
async def search_tasks(keyword: str):
    """
    Search for tasks by keyword.

    Args:
        keyword (str): The keyword to search for.

    Returns:
        List[TaskWithID]: A list of tasks that match the keyword in their title or description.
    """
    tasks = get_all_tasks()
    return [task for task in tasks if keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()]

@app.get("/task/{task_id}", response_model=TaskWithID)
async def get_task(task_id: int):
    """
    Get a task by its ID.

    Args:
        task_id (int): The ID of the task to get.

    Returns:
        TaskWithID: The task with the given ID.

    Raises:
        HTTPException: If the task with the given ID does not exist.
    """
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/task", response_model=TaskWithID)
async def create_task_endpoint(task: Task, current_user: User = Depends(get_user_from_token)):
    """
    Create a new task.

    Args:
        task (Task): The task to create.

    Returns:
        TaskWithID: The created task.

    Raises:
        HTTPException: If the current user is not found.
    """
    if current_user.username not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return create_task(task)

@app.put("/task/{task_id}", response_model=TaskWithID)
async def update_task_endpoint(task_id: int, task: Task, current_user: User = Depends(get_user_from_token)):
    """
    Update a task by its ID.

    Args:
        task_id (int): The ID of the task to update.
        task (Task): The task to update.

    Returns:
        TaskWithID: The updated task.

    Raises:
        HTTPException: If the user is not found or if the task with the given ID does not exist.
    """

    if current_user.username not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    task = modify_task(task_id, task)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/task/{task_id}", response_model=TaskWithID)
async def delete_task_endpoint(task_id: int, current_user: User = Depends(get_user_from_token)):    
    """
    Delete a task by its ID.

    Args:
        task_id (int): The ID of the task to delete.

    Returns:
        TaskWithID: The deleted task.

    Raises:
        HTTPException: If the user is not found or if the task with the given ID does not exist.
    """
    if current_user.username not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    task = delete_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
