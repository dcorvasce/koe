from .controller import *
from bcrypt import hashpw, checkpw, gensalt

class AuthController(Controller):
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
        REQUIRED_PARAMS = ['email', 'password']
        params = {}

        for param in REQUIRED_PARAMS:
            if request.form.get(param) is None:
                return dumps({'error': 'Missing %s' % param.replace('_', ' ')})
            params[param] = request.form.get(param)

        if self.__user_exists(params['email']) is False:
            return dumps({'error': 'The user does not exists'})

        user = self.database.selectAll('SELECT id, password FROM users WHERE email = %s', params['email'])[0]

        if checkpw(params['password'].encode('utf8'), user['password'].encode('utf8')) is False:
            return dumps({'error': 'Wrong password'})

        self.session['user_id'] = user['id']
        return dumps({'ok': True})

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
