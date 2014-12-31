#import the scraping libs
import requests
import urllib
from bs4 import BeautifulSoup

#get the user details
username = raw_input("Please enter the EXACT chess.com username of the user whose games you wish to download:")
userurl = "http://www.chess.com/home/game_archive?sortby=&show=live&member=%s"%username

#get the html for the relevant page,where we'll extract the game ids using BeautifulSoup
r = requests.get(userurl)
soup = BeautifulSoup(r.content)
#list for initial BeautifulSoup extract coz I don't know how to extract them directly
gameids = []

#outputs some links like : /livechess/game?id=1004499200.Bam.We got our ids
for link in soup.select('a[href^=/livechess/game?id=]'):
	gameids.append(link['href'])

#extract the actual ids into a list
newerids = []
for gameid in gameids:
	newid = gameid[-10:]
	newerids.append(newid)

#download ze freakin games.Python wins :)
for newid in newerids:
	idnum = int(newid)
	fileurl = "http://www.chess.com/echess/download_pgn?lid=%d" %idnum
	urllib.urlretrieve(fileurl,"%d.pgn" %idnum)