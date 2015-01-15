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

# Get the link to the individual ad listing
listing = soup.find('div', {'class' : 'ad-title'})
listingLnk = listing.find('a')
print listingLnk['href']

# Create output file
with open("output.csv", "wb") as csvfile:
	fileObj = csv.writer(csvfile, delimiter =',')
	fileObj.writerow(['Make/Model', 'Seller Contact #', 'Boat Price'])

print "Done."

