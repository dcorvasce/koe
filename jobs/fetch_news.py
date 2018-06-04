'''
Each N minutes, for each source registered in the system
it fetches the new articles, categorize them and store them.
'''
import sys
sys.path.append('../koe')

import pymysql
from classifier.classifier import classify
from datetime import datetime
from urllib import request
from bs4 import BeautifulSoup
from koe.db_utilities import DB
from koe.feed_utilities import user_agent

conn = pymysql.connect('localhost', 'root', 'password', 'koe', charset='utf8')
db = DB(conn, conn.cursor(pymysql.cursors.DictCursor))

sources = db.selectAll('SELECT id, rss_uri AS uri FROM sources', None)

for source in sources:
    source_id = source['id']
    req = request.Request(source['uri'], None, user_agent())

    response = request.urlopen(req)
    page = response.read()

    tree = BeautifulSoup(page, 'xml')
    items = tree.findAll('item')

    accepted_date_formats = ['%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S %Z', '%d %b %Y']

    for item in items:
        piece = {
            'source_id': source_id,
            'title': item.title.text,
            'uri': item.link.text
        }

        article_content = item.content or item.summary or item.description

        if article_content is not None:
            article_content = "%s %s" % (piece['title'], article_content.text)
        else:
            article_content = piece['title']
        piece['category'] = classify(article_content)

        if item.pubDate is not None:
            for date_format in accepted_date_formats:
                try:
                    piece['published_at'] = datetime.strptime(item.pubDate.text, date_format)
                    break
                except ValueError:
                    continue

        if piece.get('published_at') is None:
            piece['published_at'] = datetime.now()

        piece['published_at'] = piece['published_at'].strftime('%Y-%m-%d %H:%M')
        news_found = db.selectAll('SELECT id FROM articles WHERE uri = %s', piece['uri'])

        if len(news_found) == 0:
            db.insert('articles', piece)
