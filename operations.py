import csv
from typing import Optional, List
from schemas import Task, TaskWithID, taskv2WithID

#constants
CSV_FILE = "tasks.csv"

columns = ["id", "title", "description", "status"]


#-----------V2----------------
def read_all_tasks_v2() -> List[taskv2WithID]:
    """
    Reads all tasks from the csv file and returns them as a list of taskv2WithID objects

    Returns:
        list[taskv2WithID]: a list of all tasks in the csv file
    """
    with open(CSV_FILE) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return [taskv2WithID(**row) for row in csv_reader]

#-----------------------------



def get_all_tasks() -> List[TaskWithID]: 
    """
    Reads all tasks from the csv file and returns them as a list of TaskWithID objects

    Returns:
        list[TaskWithID]: a list of all tasks in the csv file
    """
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
    """
    Generates the next id for a task by reading the CSV file and returning the maximum id + 1

    Returns:
        int: The next id for a task
    """
    try:
        with open(CSV_FILE) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            return max([int(row["id"]) for row in csv_reader]) + 1
    except ValueError:
        return 1
    
def write_task_into_csv(task: TaskWithID):
    """
    Writes a task into the CSV file. If the CSV file is empty (i.e. no header), write the header first.
    Then write the task into the CSV file.

    Args:
        task (TaskWithID): The task to write into the CSV file
    """
    with open(CSV_FILE, mode="a", newline="") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=columns)
        if csv_file.tell() == 0:  # Check if file is empty
            csv_writer.writeheader()
        csv_writer.writerow(task.model_dump())

def create_task(task: Task) -> TaskWithID:
    """
    Creates a new task with a unique id and writes it into the CSV file

    Args:
        task (Task): The task to write into the CSV file

    Returns:
        TaskWithID: The task with an id
    """
    id = get_next_id()
    task_with_id = TaskWithID(id=id, **task.model_dump())
    write_task_into_csv(task_with_id)
    return task_with_id

def modify_task(id: int, task: Task) -> Optional[TaskWithID]:
    """
    Modifies a task in the CSV file.

    Args:
        id (int): The id of the task to modify
        task (Task): The new task to write into the CSV file

    Returns:
        Optional[TaskWithID]: The modified task if the task was found, None if it wasn't
    """
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
    """
    Deletes a task from the CSV file.

    Args:
        id (int): The id of the task to delete

    Returns:
        Optional[TaskWithID]: The deleted task if it existed, None if it didn't
    """
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
                