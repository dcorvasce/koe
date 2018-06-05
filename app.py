from flask import Flask, render_template, session, redirect
from config.session import start_session
from config.database import conn
from koe.controllers import *
import pymysql

app = Flask(__name__)
start_session(app)

# Routes
@app.route('/')
def index():
    if session.get('user_id') is not None:
        controller = UserController(conn, session)
        sources = controller.get_user_feeds()
        articles = controller.get_user_news()

        return render_template('index.html', sources=sources, articles=articles)
    return redirect('/signin')

@app.route('/source/new', methods=['POST'])
def new_source():
    controller = FeedController(conn, session)
    return controller.create()

@app.route('/news')
def news():
    controller = FeedController(conn, session)
    return controller.get_news()

@app.route('/signup')
def new_user():
    controller = AuthController(conn, session)
    return controller.show_register()

@app.route('/signin')
def show_sign_in():
    controller = AuthController(conn, session)
    return controller.show_login()

@app.route('/signup', methods=['POST'])
def create_user():
    controller = AuthController(conn, session)
    return controller.register()

@app.route('/signin', methods=['POST'])
def sign_in():
    controller = AuthController(conn, session)
    return controller.login()

@app.route('/signout', methods=['POST'])
def sign_out():
    session['user_id'] = None
    return redirect('/')
