import psycopg2

from source.sql.db import get_db
import uuid

def createUser(email, pic):
    conn = get_db()
    cur = conn.cursor()
    uniqueID = str(uuid.uuid4())
    try:
        cur.execute(
            "INSERT INTO users(id, email, email_picture, created_at, updated_at) "
            "VALUES(%s, %s, %s, NOW(), NOW())",
            (uniqueID, email, pic)
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()  # Always rollback on failure
        print(f"User with email {email} already exists — skipping insert.")
    return