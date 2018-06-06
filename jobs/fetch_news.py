'''
Each N minutes, for each source registered in the system
it fetches the new articles, categorize them and store them.
'''
import sys
sys.path.append('../koe')

from config.database import conn
from pymysql import cursors
from koe.db_utilities import DB
from classifier.classifier import classify
from datetime import datetime
from urllib import request
from bs4 import BeautifulSoup
from koe.feed_utilities import user_agent

db = DB(conn, conn.cursor(cursors.DictCursor))

def fetch_item_data(source_id, item):
    return {'source_id': source_id, 'title': item.title.text, 'uri': item.link.text}

def get_date_formats():
    return ['%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S %Z', '%d %b %Y']

def fetch_active_sources():
    '''Fetches only the sources which have subscriptions'''
    query = '''
            SELECT sources.id, sources.latestlink_fetched, sources.rss_uri AS uri
            FROM sources
            WHERE (SELECT COUNT(*) FROM subscriptions WHERE source_id = sources.id) > 0
            ORDER BY sources.id DESC
            '''
    return db.selectAll(query, None)

def fetch_feed_tree(source):
    req = request.Request(source['uri'], None, user_agent())
    response = request.urlopen(req)
    page = response.read()

    return BeautifulSoup(page, 'xml')

def get_article_date(item):
    accepted_date_formats = get_date_formats()
    date = datetime.now()
    published_date = item.pubDate or item.published

    if published_date is not None:
        for date_format in accepted_date_formats:
            try:
                date = datetime.strptime(published_date.text, date_format)
                break
            except ValueError:
                continue
    return date

def get_article_body(item, piece):
    content = item.content or item.summary or item.description

    if content is not None:
        content = "%s %s" % (piece['title'], content.text)
    else:
        content = piece['title']
    return content

def fetch_news():
    sources = fetch_active_sources()
    articles_fetched = 0

    for source in sources:
        print('Fetching news for %s...' % source['uri'])

        source_id = source['id']
        latestlink_fetched = source.get('latestlink_fetched')
        index_link = None

        tree = fetch_feed_tree(source)
        items = tree.findAll('item') or tree.findAll('entry')

        for item in items:
            if index_link is None:
                index_link = item.link.text

            if latestlink_fetched == index_link:
                break
            articles_fetched += 1

            piece = fetch_item_data(source_id, item)
            content = get_article_body(item, piece)
            piece['category'] = classify(content)

            piece['published_at'] = get_article_date(item)
            piece['published_at'] = piece['published_at'].strftime('%Y-%m-%d %H:%M')

            db.insert('articles', piece)
        try:
            db.query('UPDATE sources SET latestlink_fetched = %s WHERE id = %s', (index_link, source_id))
        except Exception:
            print('An error occured, unable to save the items')
    print('Articles fetched: %d' % articles_fetched)

if __name__ == '__main__':
    fetch_news()
