# webscraper.py - rough web scraper that pulls posting titles from a given 
# craigslist ad page. 
import requests
from bs4 import BeautifulSoup, SoupStrainer
import bs4

bsObj = requests.get('http://newyork.craigslist.org/search/hhh?query=apartment&sort=rel').text
soup = BeautifulSoup(bsObj, 'html.parser')

# to get results from multiple classes:
# results = soup.find_all('a', {'class' : ['i','hdrlnk']})
results = soup.find_all('a',{'class' : 'i'})


for n in results:
	lnk = 'http://newyork.craigslist.org' + n['href']
	bsObj2 = requests.get(lnk).text
	soup2 = BeautifulSoup(bsObj2, 'html.parser')
	results2 = soup2.find_all('h2', {'class' : 'postingtitle'}) #returning empty list 
	title = results2[0].text

	# print apartment prices for the listings on current page
	words = title.split()
	for w in words:
		if w.find('$') != -1:
			print w



