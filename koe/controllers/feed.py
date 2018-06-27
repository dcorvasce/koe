'''Manage the feeds stored on the application'''
from koe.feed_utilities import find_alternate
from .controller import *

class FeedController(Controller):
    '''Provide methods to manage feeds'''
    def create(self):
        '''Register a new feed source for the current user'''
        source_uri = request.args.get('url')

        if source_uri is None:
            return dumps({'error': 'Missing source URL'})

        rss = find_alternate(source_uri)

        if rss is None:
            return dumps({'error': 'Unable to find RSS'})

        if self.session.get('user_id') is None:
            return dumps({'error': 'Unauthorized request'})

        source_id = self.__create_source_unless_exists(rss)
        return self.__attach_feed_to_user(source_id)


    def get_news(self):
        '''Fetches all the news of a specific source'''
        user_id = self.session['user_id'] or 0
        source_id = request.args.get('source_id')
        category = request.args.get('category')
        starred = request.args.get('starred')
        page = request.args.get('page') or 0
        params = [user_id]

        query = '''
                SELECT articles.*, sources.icon_path, sources.id AS origin_id,
                sources.uri AS origin_uri, sources.title AS origin_title,
                IF((
                    SELECT COUNT(*) FROM user_favouritearticles
                    WHERE user_favouritearticles.user_id = subscriptions.user_id
                    AND article_id = articles.id) > 0, 1, 0) AS starred
                FROM sources, subscriptions, articles
                WHERE sources.id = subscriptions.source_id AND user_id = %s
                AND articles.source_id = subscriptions.source_id
                '''

        if source_id is not None:
            query += ' AND articles.source_id = %s'
            params.append(source_id)

        if category is not None:
            query += ' AND articles.category = %s'
            params.append(category)

        if starred is not None and starred == '1':
            query += '''
                AND (
                    SELECT COUNT(*) FROM user_favouritearticles
                    WHERE user_favouritearticles.user_id = subscriptions.user_id
                    AND article_id = articles.id
                ) > 0
            '''

        query += 'ORDER BY published_at DESC LIMIT %s,5'
        offset = int(page) * 5
        params.append(offset)

        news = self.database.select_all(query, tuple(params))
        return dumps(news, default=str)


    def __attach_feed_to_user(self, source_id):
        subscription = {'user_id': self.session['user_id'], 'source_id': source_id}

        try:
            self.database.insert('subscriptions', subscription)
        except Exception:
            return dumps({'error': "You've already subscribed"})
        return dumps({'ok': True})


    def __create_source_unless_exists(self, rss):
        query = 'SELECT id FROM sources WHERE uri = %s OR rss_uri = %s'
        sources = self.database.select_all(query, (rss['origin'], rss['uri']))

        if not sources:
            record = {
                'title': rss['title'],
                'uri': rss['origin'],
                'rss_uri': rss['uri'],
                'icon_path': rss.get('icon_path'),
                'latestlink_fetched': 'na'
            }

            if record['icon_path'] in ['', None]:
                record['icon_path'] = '/static/missing-source-logo.png'

            return self.database.insert('sources', record)
        return sources[0]['id']
