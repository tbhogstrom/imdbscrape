import csv
import sys
import re
import dateutil.parser
import requests
from bs4 import BeautifulSoup
import string



def info_grabber(s, date):
	if int(date) >= 1880 and int(date) <= 2050:
		s = s + '&y=' + str(date)
	film_info = requests.get("http://omdbapi.com/?t=" + s + "&r=xml")
	soup = BeautifulSoup(film_info.text, "lxml")
	tag = soup.root
	found = tag["response"]
	if found == "True":
		tag = soup.movie
		title = tag["title"]
		year = tag["year"]
		duration = tag["runtime"]
		age_rating = tag["rated"]
		genre = tag["genre"]
		plot = tag["plot"]
		picture = tag["poster"]
		director = tag["director"]
		writers = tag["writer"]
		actors = tag["actors"]
		imdbid = tag['imdbid']
		imdbhyperlink = '<a href="http://www.imdb.com/title/' + imdbid + '/">' + title + '</a>'
		film_details = {"hyperlink": imdbhyperlink, "IMDB ID": imdbid, "Title": title, "Year": year, "Duration": duration, "Age Rating": age_rating, "Genre": genre, "Plot": plot, "Picture": picture, "Director": director, "Writers": writers, "Actors": actors}
		#print(film_details)
		return film_details

#Take rawmovie string, remove year within paraenthesis
def remove_year(mystring):
	result = re.sub(r'\([^)]*\)', '', mystring)
	return result

def clean_symbols(s):
	s = s.replace("[", "")
	s = s.replace("]", "")
	s = s.replace("'", "")
	s.rstrip()
	return s

def add_plus(s):
	s = s.replace(" ", "+")
	s.rstrip("+")
	return s

def movie_lookup():
	with open('input.csv', encoding='utf-8-sig') as csvfile:
		inputreader = csv.reader(csvfile)
		for row in inputreader:
			rawmovie = str(row)
			try:
				year = int(rawmovie[rawmovie.find("(")+1:rawmovie.find(")")])
			except ValueError:
				year = '0'
			year = clean_symbols(str(year))
			movie = remove_year(rawmovie)
			movie_plus = clean_symbols(movie)
			movie_plus = add_plus(movie_plus)
			movie_info = info_grabber(movie_plus, year)
			if movie_info == None:
				print('could not find info, next movie!')
				continue
			with open('output.csv', 'a') as output:
				w = csv.DictWriter(output, movie_info.keys())
				w.writerow(movie_info)
			print(movie_plus)

#def imdb_request(s)
movie_lookup()
