from flask_session import Session
from dotenv import load_dotenv
from os import getenv

def start_session(app):
    app.config.update(SESSION_TYPE=getenv('SESSION_TYPE') or 'filesystem')
    Session(app)
