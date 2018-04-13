from scraper_functions import *

s3_files = ['https://s3-us-west-2.amazonaws.com/wordplaydata/songs_lists/'
            'songs.csv', 'https://s3-us-west-2.amazonaws.com/wordplaydata/s'
            'ongs_lists/so'
            'ngs2.csv', 'https://s3-us-west-2.amazonaws.com/wordplaydata/so'
            'ngs_lists/son'
            'gs3.csv']

for file in s3_files:
    genius_scrape(file)
