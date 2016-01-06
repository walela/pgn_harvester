import requests
from urlparse import urljoin
from bs4 import BeautifulSoup


def get_game_ids(username):
    '''
	Acess user's game archive page and return a list of game ids.
	'''
    try:
        base_url = 'http://www.chess.com/'
        game_ids = []
        '''
		Initialize the page 1 url and follow the pagination
		by extracting the "Next" link until it is not found
		'''
        next_page = 'http://www.chess.com/home/game_archive?sortby=&show=live&member=%s' % username
        while True:
            soup = BeautifulSoup(requests.get(next_page).content)
            for link in soup.select('a[href^=/livechess/game?id=]'):
                game_id = link['href'].split("?id=")[1]
                game_ids.append(int(game_id))
            try:
                next_page = urljoin(
                    base_url,
                    soup.select('ul.pagination li.next-on a')[0].get('href'))
            except IndexError:
                break
        return game_ids
    except Exception as e:
        print '%s' % str(e)
        return False
