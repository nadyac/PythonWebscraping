# Statricks project is a project sponsored by Statricks, an e-Commerce analytics company.
# The task is to build a web scraper using Beautiful Soup library to extract listing info
# and perfome data collection. The listing info includes Boat Maker/Model, seller contact #, and price
import requests
import csv
from bs4 import BeautifulSoup, SoupStrainer
import bs4

# Get all the boat makers/models for 800 boats listed on the site (no filters)
searchResults = requests.get('http://www.boattrader.com/search-results/').text
soup = BeautifulSoup(searchResults, 'html.parser')

# Get the links to each individual ad listings
listing = soup.find_all('div', {'class' : 'ad-title'})
for n in listing:
	listingLnk = n.find('a')

	#visit each ad listing to extract make/model
	singleAd = requests.get('http://www.boattrader.com/' + listingLnk['href']).text
	adSoup = BeautifulSoup(singleAd,'html.parser')
	table = adSoup.find('div', {'class' : 'collapsible'})
	tableItem = table.find_all('td')
	make_model = tableItem[3].text # the make and model of the boat

	# Extract the seller contact #
	seller = adSoup.find('div', {'class' : 'phone'})
	sellerNumber = seller.text # the seller's number

	# Extract the Price of the boat
	btPrice = adSoup.find('span', {'class' : 'bd-price'})
	price = btPrice.text # the price of the boat

# Create output file
with open("output.csv", "wb") as csvfile:
	fileObj = csv.writer(csvfile, delimiter =',')
	fileObj.writerow(['Make/Model', 'Seller Contact #', 'Boat Price'])

print "Done."

