import csv
from typing import Optional
from schemas import Task, TaskWithID, taskv2WithID

#constants
CSV_FILE = "tasks.csv"

columns = ["id", "title", "description", "status"]


#-----------V2----------------
def read_all_tasks_v2() -> list[taskv2WithID]:
    with open(CSV_FILE) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return [taskv2WithID(**row) for row in csv_reader]

#-----------------------------



def get_all_tasks() -> list[TaskWithID]:
    with open(CSV_FILE) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return [TaskWithID(**row) for row in csv_reader]

def get_task_by_id(id: int) -> Optional[TaskWithID]:
    """
    Check if id exists in CSV file and return it as TaskWithID

    Args:
        id (int): The id of the task to search for

    Returns:
        Optional[TaskWithID]: The task if it exists, None if it doesn't
    """
    with open(CSV_FILE) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if int(row["id"]) == id:
                return TaskWithID(**row)
    return None


#strategy to write a task

def get_next_id() -> int:
    try:
        with open(CSV_FILE) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            return max([int(row["id"]) for row in csv_reader]) + 1
    except ValueError:
        return 1
    
def write_task_into_csv(task: TaskWithID):
    with open(CSV_FILE, mode="a", newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=columns)
        if csv_file.tell() == 0:  # Check if file is empty
            csv_writer.writeheader()
        csv_writer.writerow(task.model_dump())

def create_task(task: Task) -> TaskWithID:
    id = get_next_id()
    task_with_id = TaskWithID(id=id, **task.model_dump())
    write_task_into_csv(task_with_id)
    return task_with_id

def modify_task(id: int, task: Task) -> Optional[TaskWithID]:
    updated_task : Optional[TaskWithID] = None
    tasks = get_all_tasks()
    for number, task_ in enumerate(tasks):
        if task_.id == id:
            tasks[number] = (
                updated_task
            ) = task_.model_copy(update=task.model_dump())
    
    with open(CSV_FILE, mode="w", newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=columns)
        csv_writer.writeheader()
        for task in tasks:
            csv_writer.writerow(task.model_dump())
    return updated_task

def delete_task(id: int) -> Optional[TaskWithID]:
    deleted_task : Optional[TaskWithID] = None
    tasks = get_all_tasks()
    with open(CSV_FILE, mode="w", newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=columns)
        csv_writer.writeheader()
        for task in tasks:
            if task.id == id:
                deleted_task = task
                continue
            csv_writer.writerow(task.model_dump())
    return deleted_task
                