'''Manage users across the application'''
from .controller import *

class UserController(Controller):
    '''Provide methods to manage users and their resources'''
    def unsubscribe(self, source_id):
        '''Unsubscribe the current user from a source'''
        user_id = self.session.get('user_id') or 0
        statement = 'DELETE FROM subscriptions WHERE user_id = %s AND source_id = %s'

        self.database.query(statement, (user_id, source_id))
        return dumps({'ok': True})


    def toggle_favourite_article(self, article_id):
        '''Mark an article as favourite or remove it as one'''
        user_id = self.session.get('user_id') or 0
        params = (user_id, article_id)

        statement = 'SELECT id FROM user_favouritearticles WHERE user_id = %s AND article_id = %s'
        favourites = self.database.select_all(statement, params)

        if not favourites:
            record = {'user_id': user_id, 'article_id': article_id}
            self.database.insert('user_favouritearticles', record)
        else:
            statement = 'DELETE FROM user_favouritearticles WHERE user_id = %s AND article_id = %s'
            self.database.query(statement, params)
        return dumps({'ok': True})


    def get_user_news(self):
        '''Fetches all the news the current user is subscribed to'''
        user_id = self.session.get('user_id') or 0
        query = '''
                SELECT articles.*, sources.icon_path, sources.id AS origin_id,
                sources.uri AS origin_uri, sources.title AS origin_title,
                IF((
                    SELECT COUNT(*) FROM user_favouritearticles
                    WHERE user_favouritearticles.user_id = subscriptions.user_id
                    AND article_id = articles.id) > 0, 1, 0) AS starred
                FROM sources, subscriptions, articles
                WHERE sources.id = subscriptions.source_id AND subscriptions.user_id = %s
                AND articles.source_id = subscriptions.source_id
                ORDER BY published_at DESC LIMIT 5
                '''

        return self.database.select_all(query, user_id)


    def get_user_feeds(self, user_id=None):
        '''Fetches all the feeds the current user is subscribed to'''
        user_id = user_id or self.session['user_id'] or 0
        query = '''
                SELECT sources.* FROM sources JOIN subscriptions
                ON sources.id = subscriptions.source_id AND user_id = %s
                '''

        return self.database.select_all(query, user_id)


    def get_user_favourite_articles(self, user_id=None):
        '''Fetches all the user's favourite articles'''
        user_id = user_id or self.session['user_id'] or 0
        query = '''
                SELECT articles.*, sources.icon_path, sources.id AS origin_id,
                sources.uri AS origin_uri, sources.title AS origin_title
                FROM sources, subscriptions, articles, user_favouritearticles
                WHERE sources.id = subscriptions.source_id
                AND subscriptions.user_id = user_favouritearticles.user_id
                AND articles.source_id = subscriptions.source_id
                AND user_favouritearticles.article_id = articles.id
                AND user_favouritearticles.user_id = %s
                ORDER BY user_favouritearticles.created_at DESC LIMIT 5
                '''
        return self.database.select_all(query, user_id)

    def get_user_favourites_count(self, user_id=None):
        '''Fetches all the user's favourite articles'''
        user_id = user_id or self.session['user_id'] or 0
        query = '''
                SELECT COUNT(user_favouritearticles.id) AS starred
                FROM sources, subscriptions, articles, user_favouritearticles
                WHERE sources.id = subscriptions.source_id
                AND subscriptions.user_id = user_favouritearticles.user_id
                AND articles.source_id = subscriptions.source_id
                AND user_favouritearticles.article_id = articles.id
                AND user_favouritearticles.user_id = %s

                '''

        return self.database.select_all(query, user_id)[0]['starred']


    def show_profile(self, user_id=None):
        '''Show user profile page'''
        user_id = user_id or self.session.get('user_id')
        if user_id is None:
            return redirect('/')

        query = '''
                SELECT *, DATE_FORMAT(created_at, '%%d %%b %%Y') AS registered_since
                FROM users WHERE id = %s
                '''
        rows = self.database.select_all(query, user_id)
        user = rows[0]

        favourites = self.get_user_favourite_articles(user_id)
        favourites_count = self.get_user_favourites_count(user_id)
        sources = self.get_user_feeds(user_id)

        return render_template('users/profile.html',
                               external=user_id != self.session.get('user_id'),
                               user=user, favourites=favourites, sources=sources,
                               favourites_count=favourites_count)


    def show_external_profile(self, email):
        '''Show external user profile page'''
        users = self.database.select_all('SELECT id FROM users WHERE email = %s', email)

        if not users:
            return redirect('/')
        return self.show_profile(users[0]['id'])
