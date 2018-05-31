import bs4
from urllib import request

def find_alternate(url):
    '''Given a website, tries to detect if it offers RSS feeds.
    It looks for a link element which has a type of "application/rss+xml"
    and return the URI attached to it.
    '''
    try:
        page = request.urlopen(url).read()
    except:
        return None
    
    tree = bs4.BeautifulSoup(str(page), 'html.parser')
    rss = tree.find(rel='alternate', type='application/rss+xml')

    if rss is None:
        return None

    result = {
        'title': tree.find('title').text,
        'origin': url,
        'uri': rss.get('href'),
        'icon_path': find_shortcut_icon(tree)
    }

    # If we're working with a relative path
    if result['uri'][0] == '/':
        result['uri'] = result['origin'] + result['uri']
    
    if result['icon_path'][0] == '/':
        result['icon_path'] = result['origin'] + result['icon_path']

    return result

def find_shortcut_icon(tree):
    icon = tree.find(rel='icon') or tree.find(rel='shortcut icon')

    if icon is None:
        return ''
    
    return icon.get('href')