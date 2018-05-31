import bs4
from urllib import request

def find_alternate(url):
    '''Given a website, tries to detect if it offers RSS feeds.
    It looks for a link element which has a type of "application/rss+xml"
    and return the URI attached to it.
    '''
    page = request.urlopen(url).read()
    tree = bs4.BeautifulSoup(str(page), 'html.parser')
    rss = tree.find(rel='alternate', type='application/rss+xml')

    if rss is None:
        return None

    rss_link = rss.get('href')

    if rss_link[0] == '/':
        return url + rss_link
    
    return rss_link