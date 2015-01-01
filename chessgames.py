#!/usr/bin/env python

#import the scraping libs
import requests
import urllib2
import pickle
from bs4 import BeautifulSoup

def get_game_ids(userurl, page): 
	# Access user's game archive and return list of game ids
	try:
		r = requests.get(userurl)
		soup = BeautifulSoup(r.content)
		gameids= []
		for link in soup.select('a[href^=/livechess/game?id=]'):
			gameid = link['href'].split("?id=")[1]
			gameids.append(int(gameid))
		return gameids
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

if __name__ == "__main__":
	username = raw_input("Enter chess.com username: ")
	userurl = "http://www.chess.com/home/game_archive?sortby=&show=live&member=%s"%username
	page = ""
	gameids = get_game_ids(userurl, page)
	print "\nAccessing game archive for: %s" % username
	games = get_games(gameids)
	if len(games) <> 0:
		for game in games:
			print game
		filename = "%s.p" % username
		pickle.dump(games, open(filename, "wb"))
		print "\n\nGames saved in file: %s.p" % username
		print "\nTotal games harvested: %d" % len(games)
		print "\n"
	else:
		print "\nNo games found for user: %s\n" % username

