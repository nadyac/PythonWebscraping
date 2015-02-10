# rough webscraper that displays apartment prices in NYC by visiting several listing pages
# sequentially through the next button. 
import requests
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

bsObj = requests.get('http://newyork.craigslist.org/search/hhh?query=apartment&sort=rel').text
soup = BeautifulSoup(bsObj, 'html.parser')
results = soup.find_all('a',{'class' : 'i'}) #grab links in a results page
nextBtn = soup.find('a', {'class' : 'button next'})
lnkNumber = 0

#Ge apartment prices by visiting the next few pages
while lnkNumber < 300:

	for n in results:
		#visit each individual link in a listings page
		lnk = 'http://newyork.craigslist.org' + n['href']
		lnkNumber = lnkNumber + 1
		bsObj2 = requests.get(lnk).text
		soup2 = BeautifulSoup(bsObj2, 'html.parser')
		title = getPostingTitle(soup2)

		# print apartment prices for the listings on current page
		words = title.split()
		for w in words:
			if w.find('$') != -1:
				print str(lnkNumber) + " - " + w

	#process the listings in the next page
	if nextBtn is not None:
		btnNext = nextBtn['href']
		bsObj = requests.get('http://newyork.craigslist.org' + str(btnNext)).text
		soup = BeautifulSoup(bsObj, 'html.parser')
		results = soup.find_all('a', {'class' : 'i'})
	else :
		break

	#Get the next button on the current page
	nextBtn = soup.find('a', {'class' : 'button next'})


