from flask import Flask, render_template, session, redirect
from config.session import start_session
from config.database import conn
from koe.controllers import *
import pymysql

app = Flask(__name__)
start_session(app)

@app.route('/page-not-found')
def page_not_found():
    return render_template('404.html')

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

@app.route('/subscriptions/<int:source_id>', methods=['DELETE'])
def unsubscribe(source_id):
    controller = UserController(conn, session)
    return controller.unsubscribe(source_id)

@app.route('/favourites/<int:article_id>', methods=['POST'])
def toggle_favourite_article(article_id):
    controller = UserController(conn, session)
    return controller.toggle_favourite_article(article_id)

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

@app.route('/profile', methods=['GET'])
def show_profile():
    controller = UserController(conn, session)
    return controller.show_profile()

@app.route('/profile/<string:email>', methods=['GET'])
def show_external_profile(email):
    controller = UserController(conn, session)
    return controller.show_external_profile(email)
