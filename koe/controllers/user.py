from .controller import *

class UserController(Controller):
    def unsubscribe(self, source_id):
        '''Unsubscribe the current user from a source'''
        user_id = self.session.get('user_id') or 0
        statement = 'DELETE FROM subscriptions WHERE user_id = %s AND source_id = %s'

        self.database.query(statement, (user_id, source_id))
        return dumps({'ok': True})

    def get_user_news(self):
        '''Fetches all the news the current user is subscribed to'''
        user_id = self.session.get('user_id') or 0
        query = '''
                SELECT articles.*, sources.icon_path, sources.id AS origin_id,
                sources.uri AS origin_uri, sources.title AS origin_title
                FROM sources, subscriptions, articles
                WHERE sources.id = subscriptions.source_id AND user_id = %s
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