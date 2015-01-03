#!/usr/bin/env python

import urllib2
import requests
from urlparse import urljoin
from bs4 import BeautifulSoup

def get_game_ids(username):
	'''
	Access user's game archive page and return a list of game ids.
	'''
	try:
		base_url = 'http://www.chess.com/'
		game_ids = []

		'''
		Initialize the page 1 url and follow the pagination by making an endless loop
		and extracting the "Next" link url until it is not found('soup.select' uses
		CSS-style syntax to achieve this).
		'''
		next_page = 'http://www.chess.com/home/game_archive?sortby=&show=live&member=%s'%username
		while True:
			soup = BeautifulSoup(requests.get(next_page).content)
			for link in soup.select('a[href^=/livechess/game?id=]'):
				game_id = link['href'].split("?id=")[1]
				game_ids.append(int(game_id))
			try:
				next_page = urljoin(base_url,soup.select('ul.pagination li.next-on a')[0].get('href'))
			except IndexError:
				break
		return game_ids
	except Exception as e:
		print "%s" % str(e)
		return False

def get_games(game_ids):
	'''
	Extract each game from list of ids and append them to a list. Returns list
	object of all games extracted.
	'''
	try:
		games = []
		for game_id in game_ids:
			fileurl = "http://www.chess.com/echess/download_pgn?lid=%d" % game_id
			games.append(urllib2.urlopen(fileurl).read())
		return games
	except Exception as e:
		print "%s" % str(e)
		return False

def merge_games(game_list,filename):
	'''
	Copy all game text from the extracted games list
	into a new pgn file with the specified filename
	'''
	with open(filename,"w") as mergefile:
		for game in game_list:
			mergefile.write("%s\n\n" % game)

if __name__ == "__main__":
	username = raw_input("Enter chess.com username: ")
	gameids = get_game_ids(username)
	print "\nAccessing game archive for: %s" % username
	game_list = get_games(gameids)
	if len(game_list) > 0:
		filename = "%s.pgn" % username
		merge_games(game_list,filename)
		print "\n\nGames saved in file: %s.pgn" % username
		print "\nTotal games harvested: %d" % len(game_list)
		print "\n"
	else:
		print "\nNo games found for user: %s\n" % username

