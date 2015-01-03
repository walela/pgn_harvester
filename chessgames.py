#!/usr/bin/env python

#import the scraping libs
from urlparse import urljoin
import requests
import urllib2
from bs4 import BeautifulSoup

def get_game_ids(username):
	# Access user's game archive and return list of game ids
	try:
		base_url = 'http://www.chess.com/'
		game_ids = []
		next_page = 'http://www.chess.com/home/game_archive?sortby=&show=live&member=%s'%username
		while True:
			soup = BeautifulSoup(requests.get(next_page).content)
			for link in soup.select('a[href^=/livechess/game?id=]'):
				gameid = link['href'].split("?id=")[1]
				game_ids.append(int(gameid))
			try:
				next_page = urljoin(base_url,soup.select('ul.pagination li.next-on a')[0].get('href'))
			except IndexError:
				break
		return game_ids
	except Exception as e:
		print "%s" % str(e)
		return False

def get_games(gameids):
	# Extract each game from list of ids
	try:
		games = []
		for gameid in gameids:
			fileurl = "http://www.chess.com/echess/download_pgn?lid=%d" % gameid
			games.append(urllib2.urlopen(fileurl).read())
		return games
	except Exception as e:
		print "%s" % str(e)
		return False

def merge_games(gamelist,filename):
	with open(filename,"w") as mergefile:
		for game in gamelist:
			mergefile.write("%s\n\n" %game)

if __name__ == "__main__":
	username = raw_input("Enter chess.com username: ")
	gameids = get_game_ids(username)
	print "\nAccessing game archive for: %s" % username
	games = get_games(gameids)
	if len(games) > 0:
		filename = "%s.pgn" % username
		merge_games(games,filename)
		print "\n\nGames saved in file: %s.pgn" % username
		print "\nTotal games harvested: %d" % len(games)
		print "\n"
	else:
		print "\nNo games found for user: %s\n" % username

