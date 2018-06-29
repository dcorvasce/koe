from json import dumps
from pymysql import cursors
from flask import request, redirect, render_template
from koe.db_utilities import DB

class Controller(object):
    def __init__(self, session, logger):
        self.database = DB()
        self.session = session
        self.logger = logger


    def __current_user(self):
        '''Return the current logged user'''
        user_id = self.session.get('user_id') or 0
        users_found = self.database.select_all('SELECT * FROM users WHERE id = %s', user_id)

        if not users_found:
            return None
        return users_found[0]


    def __user_exists(self, email):
        '''Given an email address, check if there is a user associated to it'''
        users_found = self.database.select_all('SELECT * FROM users WHERE email = %s', email)
        return len(users_found) > 0
