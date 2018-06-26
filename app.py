'''Defines the app routes'''
from flask import Flask, render_template, session, redirect
from config.session import start_session
from config.database import conn
from config.logging import logger
from koe.controllers import *
from sys import exc_info

app = Flask(__name__)
start_session(app)

@app.route('/')
def index():
    '''Render home page

    Return the dashboard if the user is already logged in.
    Otherwise, it returns the sign in form.
    '''
    if session.get('user_id') is not None:
        controller = UserController(conn, session, logger)
        sources = controller.get_user_feeds()
        articles = controller.get_user_news()

        return render_template('index.html', sources=sources, articles=articles)
    return redirect('/signin')


@app.route('/source/new', methods=['POST'])
def new_source():
    '''Subscribe the current user to a new source'''
    controller = FeedController(conn, session, logger)
    return controller.create()


@app.route('/subscriptions/<int:source_id>', methods=['DELETE'])
def unsubscribe(source_id):
    '''Unsubscribe the current user from a source'''
    controller = UserController(conn, session, logger)
    return controller.unsubscribe(source_id)


@app.route('/favourites/<int:article_id>', methods=['POST'])
def toggle_favourite_article(article_id):
    '''Given the article, either mark it as favourite or not'''
    controller = UserController(conn, session, logger)
    return controller.toggle_favourite_article(article_id)


@app.route('/news')
def news():
    '''Return news the current user is subscribed to

    It allows the user to filter news by source and category.
    '''
    controller = FeedController(conn, session, logger)
    return controller.get_news()


@app.route('/signup')
def new_user():
    '''Show sign up form'''
    controller = AuthController(conn, session, logger)
    return controller.show_register()


@app.route('/signin')
def show_sign_in():
    '''Show sign in form'''
    controller = AuthController(conn, session, logger)
    return controller.show_login()


@app.route('/signup', methods=['POST'])
def create_user():
    '''Create a new user and sign her in the system'''
    controller = AuthController(conn, session, logger)
    return controller.register()


@app.route('/signin', methods=['POST'])
def sign_in():
    '''Sign in a registered user'''
    controller = AuthController(conn, session, logger)
    return controller.login()


@app.route('/signout', methods=['POST'])
def sign_out():
    '''Sign out the current user'''
    session['user_id'] = None
    return redirect('/')


@app.route('/profile', methods=['GET'])
def show_profile():
    '''Return the profile page for the current user'''
    controller = UserController(conn, session, logger)
    return controller.show_profile()


@app.route('/profile/<string:email>', methods=['GET'])
def show_external_profile(email):
    '''Return the profile page of one of the registered users'''
    controller = UserController(conn, session, logger)
    return controller.show_external_profile(email)

if __name__ == '__main__':
    logger.info('Starting Koe on 0.0.0.0:80')

    try:
        app.run(host='0.0.0.0')
    except Exception:
        logger.error('Unable to start Koe on 0.0.0.0:80 -- %s' % exc_info())
