import csv
import os
from pathlib import Path
from unittest.mock import patch

import pytest

TEST_DATABASE_FILE = "test_tasks.csv"

TEST_TASKS_CSV = [
    {
        "id": "1",
        "title": "Test Task One",
        "description": "Test Description One",
        "status": "Incomplete"
    },
    {
        "id": "2",
        "title": "Test Task Two",
        "description": "Test Description Two",
        "status": "On-going"
        
    }
]

TEST_TASKS_CSV_V2 = [
    {
        "id": "1",
        "title": "Test Task One",
        "description": "Test Description One",
        "status": "Incomplete",
        "priority": "lower"
    },
    {
        "id": "2",
        "title": "Test Task Two",
        "description": "Test Description Two",
        "status": "On-going",
        "priority": "lower"
        
    }
]

TEST_TASKS_V2 = [
    {**task_json, "id": int(task_json["id"])}
    for task_json in TEST_TASKS_CSV_V2
]

TEST_TASKS = [
    {**task_json, "id": int(task_json["id"])}
    for task_json in TEST_TASKS_CSV
]


@pytest.fixture(autouse=True)
def create_test_database():
    """
    Pytest fixture to automatically create a test database
    before all tests. The database is removed after all tests
    are finished.

    The database is created in the same directory as the
    test file and is named "test_database.csv".

    The test database is populated with the tasks in
    TEST_TASKS_CSV.

    The fixture patches the operations.CSV_FILE to point to
    the test database, and yields the patched object.

    The fixture is autouse, meaning it is automatically run
    before every test without needing to be explicitly
    referenced in the test function.

    :return: The patched operations.CSV_FILE
    :rtype: unittest.mock.MagicMock
    """
    database_file_location = str(
        Path(__file__).parent / TEST_DATABASE_FILE
    )
    with patch(
        "operations.CSV_FILE",
        database_file_location,
    ) as csv_test:
        with open(
            database_file_location, mode="w", newline=""
        ) as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=[
                    "id",
                    "title",
                    "description",
                    "status",
                ],
            )
            writer.writeheader()
            writer.writerows(TEST_TASKS_CSV)
            print("")
        yield csv_test
        os.remove(database_file_location)