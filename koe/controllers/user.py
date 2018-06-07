from .controller import *

class UserController(Controller):
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
        favourites = self.database.selectAll(statement, params)

        if len(favourites) == 0:
            self.database.insert('user_favouritearticles', {'user_id': user_id, 'article_id': article_id})
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
                ORDER BY published_at DESC LIMIT 20
                '''
        
        return self.database.selectAll(query, user_id)

    def get_user_feeds(self):
        '''Fetches all the feeds the current user is subscribed to'''
        user_id = self.session['user_id'] or 0
        query = '''
                SELECT sources.* FROM sources JOIN subscriptions
                ON sources.id = subscriptions.source_id AND user_id = %s
                '''

        return self.database.selectAll(query, user_id)
    
    def get_user_favourite_articles(self):
        '''Fetches all the user's favourite articles'''
        user_id = self.session['user_id'] or 0
        query = '''
                SELECT articles.*, sources.icon_path, sources.id AS origin_id,
                sources.uri AS origin_uri, sources.title AS origin_title
                FROM sources, subscriptions, articles, user_favouritearticles
                WHERE sources.id = subscriptions.source_id
                AND subscriptions.user_id = user_favouritearticles.user_id
                AND articles.source_id = subscriptions.source_id
                AND user_favouritearticles.article_id = articles.id
                AND user_favouritearticles.user_id = %s
                ORDER BY user_favouritearticles.created_at DESC LIMIT 20
                '''
        return self.database.selectAll(query, user_id)

    def show_profile(self):
        '''Show user profile page'''
        user_id = self.session.get('user_id')
        if user_id is None:
            return redirect('/')
        
        query = '''
                SELECT *, DATE_FORMAT(created_at, '%%d %%b %%Y') AS registered_since
                FROM users WHERE id = %s
                '''
        rows = self.database.selectAll(query, user_id)
        user = rows[0]

        favourites = self.get_user_favourite_articles()
        sources = self.get_user_feeds()
        return render_template('users/profile.html', user=user,
                                                     favourites=favourites, sources=sources)
