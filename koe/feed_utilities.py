'''Provide utility functions to manage feeds'''
from urllib import request, error
import bs4

def user_agent():
    '''Return a fake user agent for HTTP requests'''
    agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; \
             rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    return {'User-Agent': agent}


def find_alternate(url):
    '''Given a website, fetch data about its RSS version

    It looks for a 'link' element which has a type of "application/rss+xml"
    if the page is an HTML one. Otherwise, parse the RSS document
    fetching the needed information.
    '''
    try:
        req = request.Request(url, None, user_agent())

        response = request.urlopen(req)
        page = response.read()
    except error.URLError:
        return None

    content_type = response.info().get_content_type()
    parser_type = 'html.parser'

    if 'xml' in content_type:
        parser_type = 'xml'

    tree = bs4.BeautifulSoup(page, parser_type)

    if parser_type == 'xml':
        return fetch_xml_info(tree, url)
    return fetch_html_info(tree, url)


def fetch_xml_info(tree, url):
    '''Fetch information about the RSS feed from the RSS document itself'''
    result = {
        'title': tree.channel.title.text,
        'origin': tree.channel.link.text,
        'uri': url,
        'icon_path': ''
    }

    # Fetch the shortcut icon
    req = request.Request(result['origin'], None, user_agent())

    page = request.urlopen(req).read()
    html = bs4.BeautifulSoup(page, 'html.parser')

    result['icon_path'] = find_shortcut_icon(html, result['origin'])
    return result


def fetch_html_info(tree, url):
    '''Fetch information about the RSS feed from the HTML page'''
    rss = tree.find(rel='alternate', type='application/rss+xml')

    if rss is None:
        return None

    result = {
        'title': tree.find('title').text,
        'origin': url,
        'uri': rss.get('href'),
        'icon_path': find_shortcut_icon(tree, url)
    }

    # If we're working with a relative path
    if result['uri'][0] == '/':
        result['uri'] = result['origin'] + result['uri']

    return result


def find_shortcut_icon(tree, url):
    '''Try to find the source's icon

    If an icon is found, it'll be used in the dashboard to mark the source.
    Otherwise, a placeholder icon will be used.
    '''
    icon = tree.find(rel='icon') or tree.find(rel='shortcut icon')

    if icon is None:
        return ''

    icon_uri = icon.get('href')

    if icon_uri[0] == '/':
        return url + icon_uri
    return icon_uri
