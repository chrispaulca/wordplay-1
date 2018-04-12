from scraper_functions import *

try:
	for files in ['songs1.csv', 'songs2.csv', 'songs3.csv']:
	    genius_scrape(files)
except:
	print('need to pull from s3')
