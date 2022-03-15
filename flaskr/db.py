# database information and access
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():  # configure our db
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # возвращает данныз из базы в виде словоря

    return g.db


'''
"g" is a special object that is unique for each request. 
It is used to store data that might be accessed by multiple functions during the request. 
The connection is stored and reused instead of creating a new connection 
if get_db is called a second time in the same request.
'''


def close_db(e=None):  # close our db
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():  # open and use our db
    """  "get_db" returns a database connection, which is used to execute the commands read from the file.   """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))  # передаем команды в субд


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):  # takes the application and does the registration
    app.teardown_appcontext(close_db)  # tells Flask to call that function when cleaning up after returning the response
    app.cli.add_command(init_db_command)  # adds a new command that can be called with the flask command


# we can initialize the database with "init-db" command
