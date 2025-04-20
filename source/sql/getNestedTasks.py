import psycopg2
from source.sql.db import get_db

from psycopg2.extras import RealDictCursor

def getNestedTasks(email):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)  # 👈 this makes each row a dict
    try:
        cur.execute("""
            WITH RECURSIVE task_tree AS (
                SELECT 
                    task_id, title, \"desc\", parent_id, task_id AS root_id, 0 AS depth
                FROM tasks
                WHERE parent_id IS NULL AND email = %s
                UNION ALL
                SELECT 
                    t.task_id, t.title, t.desc, t.parent_id, tt.root_id, tt.depth + 1
                FROM tasks t
                JOIN task_tree tt ON t.parent_id = tt.task_id
            )
            SELECT * FROM task_tree ORDER BY root_id, depth
        """, (email,))
        return cur.fetchall()  # already dicts!
    except Exception as e:
        conn.rollback()
        print("DB Error:", e)
        return []

