'''Initialize the application session system'''
from os import getenv
from flask_session import Session


def start_session(app):
    '''Start the session system for the given Flask application'''
    app.config.update(SESSION_TYPE=getenv('SESSION_TYPE') or 'filesystem')
    Session(app)
