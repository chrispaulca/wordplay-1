from scraper_functions import *

<<<<<<< HEAD
s3_files = ['https://s3-us-west-2.amazonaws.com/wordplaydata/songs_lists/'
            'songs.csv', 'https://s3-us-west-2.amazonaws.com/wordplaydata/s'
            'ongs_lists/so'
            'ngs2.csv', 'https://s3-us-west-2.amazonaws.com/wordplaydata/so'
            'ngs_lists/son'
            'gs3.csv']

for file in s3_files:
    genius_scrape(file)
=======
try:
	for files in ['songs1.csv', 'songs2.csv', 'songs3.csv']:
	    genius_scrape(files)
except:
	print('need to pull from s3')
>>>>>>> 89fb703d27d9c1d96ba497bcc2fb3683ae0c2e67
