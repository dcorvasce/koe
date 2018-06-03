from flask import Flask, render_template, session, redirect
from config.session import start_session
from config.database import conn
from koe.controllers.feed import FeedController
from koe.controllers.user import UserController
import pymysql

app = Flask(__name__)
start_session(app)

# Routes
@app.route('/')
def index():
    if session.get('user_id') is not None:
        controller = FeedController(conn, session)
        sources = controller.get_user_feeds()
        articles = controller.get_user_news()

        return render_template('index.html', sources=sources, articles=articles)
    return redirect('/signin')

@app.route('/source/new', methods=['POST'])
def new_source():
    controller = FeedController(conn, session)
    return controller.create()

@app.route('/news/<source>')
def news_by_source(source):
    controller = FeedController(conn, session)
    return controller.get_news_by_source(source)

@app.route('/signup')
def new_user():
    controller = UserController(conn, session)
    return controller.new()

@app.route('/signin')
def show_sign_in():
    controller = UserController(conn, session)
    return controller.show_sign_in()

@app.route('/signup', methods=['POST'])
def create_user():
    controller = UserController(conn, session)
    return controller.create()

@app.route('/signin', methods=['POST'])
def sign_in():
    controller = UserController(conn, session)
    return controller.sign_in()

@app.route('/signout', methods=['POST'])
def sign_out():
    session['user_id'] = None
    return redirect('/')