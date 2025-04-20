import psycopg2
from source.sql.db import get_db
import uuid

def createTask(email, title, desc, time, parentID=None, complete=None):
    conn = get_db()
    cur = conn.cursor()
    uniqueID = str(uuid.uuid4())
    try:
        cur.execute(
            "INSERT INTO tasks(task_id, email, parent_id, title, \"desc\", time, created_at, updated_at, complete) "
            "VALUES(%s, %s, %s, %s, %s, %s, NOW(), NOW(), %s)",
            (uniqueID, email, parentID, title, desc, time, complete)
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()  # Always rollback on failure
        print("Could not create task")
    return