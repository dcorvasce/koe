from flask import Flask, render_template
from koe.db_utilities import DB
from koe.controllers.feed import FeedController
import pymysql

app = Flask(__name__)
conn = pymysql.connect('localhost', 'root', 'password', 'koe')
db = DB(conn, conn.cursor(pymysql.cursors.DictCursor))

# Routes

@app.route('/')
def index():
    return render_template('index.html', sources=[])

@app.route('/source/new', methods=['POST'])
def new_source():
    controller = FeedController(db)
    return controller.create()
