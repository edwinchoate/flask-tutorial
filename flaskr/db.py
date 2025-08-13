import sqlite3
from flask import g, current_app

# g is a shared object that allows you to share and re-use data (such as a db connection) across requests

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        # sqlite3.Row means return rows that behave like dicts. This allows accessing columns by name.
        g.db.row_factory = sqlite3.Row 
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if g.db is not None:
        db.close()
