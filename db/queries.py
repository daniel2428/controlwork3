CREATE_TABLE_TASKS = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    completed INTEGER DEFAULT 0
)
"""

SELECT_ALL = "SELECT id, task, completed FROM tasks"
SELECT_COMPLETED = "SELECT id, task, completed FROM tasks WHERE completed = 2"
SELECT_IN_WORK = "SELECT id, task, completed FROM tasks WHERE completed = 1"
SELECT_INCOMPLETE = "SELECT id, task, completed FROM tasks WHERE completed = 0"

UPDATE_STATUS = "UPDATE tasks SET completed = ? WHERE id = ?"

INSERT_TASK = "INSERT INTO tasks (task) VALUES (?)"
DELETE_TASK = "DELETE FROM tasks WHERE id = ?"

DELETE_COMLETED = "DELETE FROM tasks WHERE completed = 2"