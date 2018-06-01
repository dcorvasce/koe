from flask import request
from json import dumps
from koe.feed_utilities import find_alternate

class FeedController(object):
    def __init__(self, database, session):
        self.database = database
        self.session = session
    
    def create(self):
        '''Register a new feed source for the current user'''
        source_uri = request.args.get('url')

        if source_uri is None:
            return dumps({'error': 'Missing source URL'})
    
        rss = find_alternate(source_uri)

        if rss is None:
            return dumps({'error': 'Unable to find RSS'})
    
        source_id = self.__create_source_unless_exists(rss)
        return self.__attach_feed_to_user(source_id)
    
    def get_user_news(self):
        '''Fetches all the news the current user is subscribed to'''
        user_id = self.session['user_id']
        query = '''
                SELECT articles.*, sources.icon_path,
                sources.uri AS origin_uri, sources.title AS origin_title
                FROM sources, subscriptions, articles
                WHERE sources.id = subscriptions.source_id AND user_id = %s
                AND articles.source_id = subscriptions.source_id
                ORDER BY published_at LIMIT 50
                '''
        
        return self.database.selectAll(query, user_id)

    def get_user_feeds(self):
        '''Fetches all the feeds the current user is subscribed to'''
        user_id = self.session['user_id']
        query = '''
                SELECT sources.* FROM sources JOIN subscriptions
                ON sources.id = subscriptions.source_id AND user_id = %s
                '''

        return self.database.selectAll(query, user_id)

    def __attach_feed_to_user(self, source_id):
        subscription = {'user_id': self.session['user_id'], 'source_id': source_id}
        
        try:
            self.database.insert('subscriptions', subscription)
        except Exception:
            return dumps({'error': "You've already subscribed"})
        return dumps({'ok': True})

    def __create_source_unless_exists(self, rss):
        query = 'SELECT id FROM sources WHERE uri = %s'
        sources = self.database.selectAll(query, rss['origin'])

        if len(sources) == 0:
            record = {
                'title': rss['title'],
                'uri': rss['origin'],
                'rss_uri': rss['uri'],
                'icon_path': rss['icon_path']
            }
            return self.database.insert('sources', record)
        return sources[0]['id']
