from flask import request
from json import dumps, loads
from koe.feed_utilities import find_alternate

class FeedController(object):
    def __init__(self, database):
        self.database = database
    
    def create(self):
        source_uri = request.args.get('url')

        if source_uri is None:
            return dumps({'error': 'Missing source URL'})
    
        rss = find_alternate(source_uri)

        if rss is None:
            return dumps({'error': 'Unable to find RSS'})
    
        self._create_feed_unless_exists(rss)
        return dumps({'ok': True, 'rss': rss['uri']})
    
    def _create_feed_unless_exists(self, rss):
        query = 'SELECT id FROM sources WHERE uri = %s'
        sources = self.database.selectAll(query, rss['origin'])

        if len(sources) == 0:
            record = {
                'title': rss['title'],
                'uri': rss['origin'],
                'rss_uri': rss['uri'],
                'icon_path': rss['icon_path']
            }
            self.database.insert('sources', record)
