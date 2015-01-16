# Statricks project is a project sponsored by Statricks, an e-Commerce analytics company.
# The task is to build a web scraper using Beautiful Soup library to extract listing info
# and perfome data collection. The listing info includes Boat Maker/Model, seller contact #, and price
import requests
import csv
from bs4 import BeautifulSoup, SoupStrainer
import bs4

# Extract the make and model
def getMakeModel(soup):
	table = soup.find('div', {'class' : 'collapsible'})
	if table is not None:
		tableItem = table.find_all('td')
		make_model = tableItem[3].text # the make and model of the boat
	else: 
		make_model = ""
	return make_model

# Extract the seller contact #
def getSellerNumber(soup):
	seller = soup.find('div', {'class' : 'phone'})
	if seller is not None:
		sellerNumber = seller.text # the seller's number
	else:
		sellerNumber = ""
	return sellerNumber

# Extract the Price of the boat
def getPrice(soup):
	btPrice = soup.find('span', {'class' : 'bd-price'})
	if btPrice is not None:
		price = btPrice.text.strip() # the price of the boat
	else:
		price = ""
	return price

# Get all the boat makers/models for 800 boats listed on the site (no filters)
searchResults = requests.get('http://www.boattrader.com/search-results/').text
soup = BeautifulSoup(searchResults, 'html.parser')
number_of_listings = 0;

# Create output file
with open("output.csv", "wb") as csvfile:
	fileObj = csv.writer(csvfile, delimiter =',')

	while number_of_listings < 800:
		# Get the links to each individual ad listings on current page
		listings = soup.find_all('div', {'class' : 'ad-title'})

		for n in listings:
			listingLnk = n.find('a')
			number_of_listings = number_of_listings + 1

			#visit each ad listing to extract make/model
			singleAd = requests.get('http://www.boattrader.com/' + listingLnk['href']).text
			adSoup = BeautifulSoup(singleAd,'html.parser')

			# Extract the make and model
			make_model = getMakeModel(adSoup)

			# Extract the seller contact #
			sellerNumber = getSellerNumber(adSoup)

			# Extract the Price of the boat
			price = getPrice(adSoup)

			print str(number_of_listings) + " - " + make_model + " " + sellerNumber + " " + price
			fileObj.writerow([make_model, sellerNumber, price])

		# Get listings on the next page
		nextPage = soup.find('a', {'title' : 'Next Page'})

		if nextPage is not None:
			searchResults = requests.get('http://www.boattrader.com' + nextPage['href']).text
			soup = BeautifulSoup(searchResults, 'html.parser')
		else:
			break

print "Done."

