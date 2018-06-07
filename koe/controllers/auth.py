'''Manage the authentication across the application'''
from bcrypt import hashpw, checkpw, gensalt
from .controller import *

class AuthController(Controller):
    '''Provide methods to manage authentication and accesses'''
    def show_login(self):
        '''Show the sign in form for an existing user'''
        if self.__current_user() is not None:
            return redirect('/')
        return render_template('users/login.html')


    def show_register(self):
        '''Show the sign up form for a new user'''
        if self.__current_user() is not None:
            return redirect('/')
        return render_template('users/new.html')


    def register(self):
        '''Create a new user'''
        required_params = ['first_name', 'last_name', 'email', 'password']
        user = {}

        for param in required_params:
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
        required_params = ['email', 'password']
        params = {}

        for param in required_params:
            if request.form.get(param) is None:
                return dumps({'error': 'Missing %s' % param.replace('_', ' ')})
            params[param] = request.form.get(param)

        if self.__user_exists(params['email']) is False:
            return dumps({'error': 'The user does not exists'})

        query = 'SELECT id, password FROM users WHERE email = %s'
        user = self.database.select_all(query, params['email'])[0]

        if checkpw(params['password'].encode('utf8'), user['password'].encode('utf8')) is False:
            return dumps({'error': 'Wrong password'})

        self.session['user_id'] = user['id']
        return dumps({'ok': True})


    def __current_user(self):
        '''Returns the current logged user'''
        user_id = self.session.get('user_id') or 0
        users_found = self.database.select_all('SELECT * FROM users WHERE id = %s', user_id)

        if not users_found:
            return None
        return users_found[0]


    def __user_exists(self, email):
        users_found = self.database.select_all('SELECT * FROM users WHERE email = %s', email)
        return len(users_found) > 0
