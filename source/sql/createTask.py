import psycopg2
from source.sql.db import get_db
import uuid

def createTask(email, title, desc, date, time, parentID=None, complete=None):
    conn = get_db()
    cur = conn.cursor()
    uniqueID = str(uuid.uuid4())
    try:
        cur.execute(
            "INSERT INTO tasks(task_id, email, parentID, title, desc, date, time, created_at, updated_at) "
            "VALUES(%s, %s, %s, %s, %s, %s, %s NOW(), NOW())",
            (uniqueID, email, parentID, title, desc, date, time, complete)
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()  # Always rollback on failure
        print("Could not create task")
    return