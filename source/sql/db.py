import psycopg2
from flask import g
from server import app

def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(app.config['POSTGRES_URL'])
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db:
        db.close()