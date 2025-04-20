from db import get_db
import uuid

def createUser(email):
    conn = get_db()
    cur = conn.cursor()
    uniqueID = str(uuid.uuid4())
    cur.execute("INSERT INTO users(id, email, created_at, updated_at)"
                +"VALUES(%s, %s, NOW(), NOW())", (uniqueID, email)
                )

    conn.commit()
