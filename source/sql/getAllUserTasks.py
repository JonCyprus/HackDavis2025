import psycopg2
from source.sql.db import get_db
import uuid

def getAllUserTasks(email):
    conn = get_db()
    cur = conn.cursor()
    results = None
    try:
        cur.execute("SELECT * FROM tasks WHERE email = %s", (email,))
        results = cur.fetchall()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()  # Always rollback on failure
        print(f"Could not get tasks for %s", email)

    return results