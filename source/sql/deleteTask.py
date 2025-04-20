import psycopg2
from source.sql.db import get_db

def deleteTask(email, taskTitle):
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "DELETE FROM tasks WHERE title = %s AND email = %s", (taskTitle, email)
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()  # Always rollback on failure
        print("Could not delete task")
    return