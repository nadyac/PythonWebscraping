# rough webscraper that displays apartment prices in NYC by visiting several listing pages
# sequentially through the next button. 
import requests
import requests.exceptions
from bs4 import BeautifulSoup, SoupStrainer
import bs4

#Get the posting title
def getPostingTitle(soup):
	posting_title = soup.find_all('h2', {'class' : 'postingtitle'})
	if posting_title is not None:
		title = posting_title[0].text
	else:
		title = ""
	return title

def getPrices(title):
	# print apartment prices for the listings on current page
	words = title.split()
	for w in words:
		if w.find('$') != -1:
			print str(lnkNumber) + " - " + w

try:
	request_object = requests.get('http://newyork.craigslist.org/search/hhh?query=apartment&sort=rel').text
	soup = BeautifulSoup(request_object, 'html.parser')
	results = soup.find_all('a',{'class' : 'i'}) #grab links in a results page
	nextBtn = soup.find('a', {'class' : 'button next'})
	lnkNumber = 0

	#Ge apartment prices by visiting the next few pages
	while lnkNumber < 300:

		for n in results:
			#visit each individual link in a listings page
			lnk = 'http://newyork.craigslist.org' + n['href']
			lnkNumber = lnkNumber + 1
			single_ad = requests.get(lnk).text
			soup2 = BeautifulSoup(single_ad, 'html.parser')
			title = getPostingTitle(soup2)

			#get apartment prices
			getPrices(title)

		#process the listings in the next page
		if nextBtn is not None:
			btnNext = nextBtn['href']
			request_object = requests.get('http://newyork.craigslist.org' + str(btnNext)).text
			soup = BeautifulSoup(request_object, 'html.parser')
			results = soup.find_all('a', {'class' : 'i'})
		else :
			break

		#Get the next button on the current page
		nextBtn = soup.find('a', {'class' : 'button next'})
except requests.exceptions.RequestException as e:
	print "There was an error with the connection. Please try again."
	single_ad.raise_for_status()
	print e




