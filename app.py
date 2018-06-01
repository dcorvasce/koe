from flask import Flask, render_template, session
from koe.db_utilities import DB
from koe.controllers.feed import FeedController
from koe.controllers.user import UserController
from flask_session import Session
import pymysql

# Configuration

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
conn = pymysql.connect('localhost', 'root', 'password', 'koe', charset='utf8')
db = DB(conn, conn.cursor(pymysql.cursors.DictCursor))

# Routes

@app.route('/')
def index():
    if session.get('user_id') is not None:
        return render_template('index.html', sources=[])
    return render_template('users/new.html')

@app.route('/source/new', methods=['POST'])
def new_source():
    controller = FeedController(db)
    return controller.create()

@app.route('/signup')
def new_user():
    controller = UserController(db, session)
    return controller.new()

@app.route('/signup', methods=['POST'])
def create_user():
    controller = UserController(db, session)
    return controller.create()