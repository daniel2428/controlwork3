CREATE_TABLE_TASKS = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    bought INTEGER DEFAULT 0
)
"""

SELECT_ALL = "SELECT id, task, bought FROM tasks"
SELECT_BOUGHT = "SELECT id, task, bought FROM tasks WHERE bought = 2"
SELECT_NEED_BOUGHT = "SELECT id, task, bought FROM tasks WHERE bought = 1"
SELECT_DOESNT_BOUHGT = "SELECT id, task, bought FROM tasks WHERE bought = 0"

UPDATE_STATUS = "UPDATE tasks SET bought = ? WHERE id = ?"

INSERT_TASK = "INSERT INTO tasks (task) VALUES (?)"
DELETE_TASK = "DELETE FROM tasks WHERE id = ?"

DELETE_BOUGHT = "DELETE FROM tasks WHERE bought = 2"