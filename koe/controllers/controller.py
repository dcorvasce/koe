from flask import request, redirect, render_template
from json import dumps
from pymysql import cursors
from koe.db_utilities import DB

class Controller(object):
    def __init__(self, db_connection, session):
        self.database = DB(db_connection, db_connection.cursor(cursors.DictCursor))
        self.session = session

    def __current_user(self):
        '''Returns the current logged user'''
        user_id = self.session.get('user_id') or 0
        users_found = self.database.selectAll('SELECT * FROM users WHERE id = %s', user_id)

        if len(users_found) == 0:
            return None
        return users_found[0]

    def __user_exists(self, email):
        users_found = self.database.selectAll('SELECT * FROM users WHERE email = %s', email)
        return len(users_found) > 0
