# rough webscraper that displays apartment prices in NYC by visiting several listing pages
# sequentially through the next button. 
import requests
from bs4 import BeautifulSoup, SoupStrainer
import bs4

bsObj = requests.get('http://newyork.craigslist.org/search/hhh?query=apartment&sort=rel').text
soup = BeautifulSoup(bsObj, 'html.parser')
results = soup.find_all('a',{'class' : 'i'})
nextBtn = soup.find('a', {'class' : 'button next'})
lnkNumber = 0

#Ge apartment prices by visiting the next few pages
while lnkNumber < 300:

	for n in results:
		lnk = 'http://newyork.craigslist.org' + n['href']
		lnkNumber = lnkNumber + 1
		bsObj2 = requests.get(lnk).text
		soup2 = BeautifulSoup(bsObj2, 'html.parser')
		results2 = soup2.find_all('h2', {'class' : 'postingtitle'})
		title = results2[0].text

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


