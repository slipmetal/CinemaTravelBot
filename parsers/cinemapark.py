#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
from collections import namedtuple
import os.path
import time
from datetime import datetime

Session = namedtuple('Session', "price booking formatD")

def get_shedules(theathres):
	return list(map(lambda kv: (kv[0], get_shedule(kv[1])), theathres.items()))

def get_shedule(theathre):
	shedule = {}
	sessions_soup = theathre.find_all('a', {'class', "btn btn-default btn-session"})
	for session_soup in sessions_soup:
		booking = session_soup.get('href')
		time 	= session_soup.find('div', {'class', "btn-session__time"}).text
		price 	= session_soup.find('div', {'class', "btn-session__price"}).text
		session_format = session_soup.find('div', {'class', "btn-session__format"}).text
		
		shedule[time] = Session(price, booking, session_format)
	
	return shedule

def get_theatres(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "lxml")

	shedule_inner = soup.find_all('div', {'class', 'schedule_row_item'})
	theathres = {}
	for theathre in shedule_inner:
		name_theatre = theathre.find('a').text
		theathres[name_theatre] = theathre

	return theathres
		
		

def get_films():
	with open("main.html",'r') as page:
		soup = BeautifulSoup(page, "lxml")
	film_list = soup.find_all('a', {'class': 'afisha-item afisha-film'})

	films = {}
	for film in film_list:
		href = film.get('href')
		name_film = film.find('div', {'class', 'afisha-film-inner'}).find('div',{'class', 'film-title'}).text
		films[name_film.lower()] = href

	return films

def download_page(url):
	response = requests.get(url + "/quick/")

	with open("main.html", 'w') as page:
		page.write(response.text)

def update_page(url):
	now = datetime.now()
	print("{} {}".format(now.weekday(), now.hour))
	if int(now.weekday()) == 3 and int(now.hour) == 8:
		download_page(url)

def main():
	url = 'http://www.cinemapark.ru'
	update_page(url)
	name = "Пятьдесят оттенков свободы"

	films = get_films()
	href = films.get(name.lower())

	if href:
		theathres = get_theatres(url + href)
		shedules = get_shedules(theathres)
		print([shedule[0] for shedule in shedules])
	

if __name__ == '__main__':
	main()