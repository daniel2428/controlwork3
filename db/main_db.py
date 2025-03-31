import sqlite3
from config import DB_PATH
from db import queries


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TABLE_TASKS)
    conn.commit()
    conn.close()


def get_tasks(filter_type="all"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if filter_type == 'completed':
        cursor.execute(queries.SELECT_COMPLETED)
    elif filter_type == 'incomplete':
        cursor.execute(queries.SELECT_INCOMPLETE)
    elif filter_type == 'inwork':
        cursor.execute(queries.SELECT_IN_WORK)
    else:
        cursor.execute(queries.SELECT_ALL)

    tasks = cursor.fetchall()
    conn.close()
    return tasks


def add_task_db(task):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_TASK, (task,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def update_task_db(task_id, new_task=None, completed=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if new_task is not None:
        cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
    if completed is not None:
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))

    conn.commit()
    conn.close()


def update_task_status(task_id, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.UPDATE_STATUS, (status, task_id))
    conn.commit()
    conn.close()


def delete_task_db(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()

def delete_completed_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_COMLETED)
    conn.commit()
    conn.close()