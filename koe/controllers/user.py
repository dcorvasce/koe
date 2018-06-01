from flask import request, render_template, redirect
from json import dumps
from bcrypt import hashpw, checkpw, gensalt

class UserController(object):
    def __init__(self, database, session):
        self.database = database
        self.session = session
    
    def new(self):
        '''Show the sign up form for a new user'''
        return render_template('users/new.html')

    def create(self):
        '''Create a new user'''
        REQUIRED_PARAMS = ['first_name', 'last_name', 'email', 'password']
        user = {}

        for param in REQUIRED_PARAMS:
            if request.form.get(param) is None:
                return dumps({'error': 'Missing %s' % param.replace('_', ' ')})
            user[param] = request.form.get(param)

            if param == 'password':
                user[param] = hashpw(user[param].encode('utf8'), gensalt())

        if self.__user_exists(user['email']):
            return dumps({'error': 'The email is already taken'})

        user_id = self.database.insert('users', user)
        self.session['user_id'] = user_id

        return dumps({'ok': True})

    def login(self):
        '''Sign in an existing user'''
        pass

    def __user_exists(self, email):
        users_found = self.database.selectAll('SELECT * FROM users WHERE email = %s', email)
        return len(users_found) > 0
