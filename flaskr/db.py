import sqlite3
from flask import g, current_app
import click


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def init_db(): 
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# g is a shared object that allows you to share and re-use data (such as a db connection) across requests

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        # sqlite3.Row means return rows that behave like dicts. This allows accessing columns by name.
        g.db.row_factory = sqlite3.Row 
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@click.command('init_db')
def init_db_command():
    """Create all tables in the database (if they don't already exist)"""
    init_db()
    click.echo('Initialized the database')


# tells Python how to interpret timestamp values in the database:convert the value to a datetime.datetime
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)
