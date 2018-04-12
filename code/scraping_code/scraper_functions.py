import pandas as pd
import numpy as np
import glob
import selenium
from random import randint
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sqlite3
from os.path import expanduser
import os
import codecs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


Path2ChromeDriverEXE = '/Users/chrispaul/Desktop/chromedriver'


def cutt(s, n):
    """Retrieve first n words of a string sentence s."""
    return ' '.join(s.split()[:n])


def genius_scrape(document):
    """Takes song info and attempts to grab its lyrics from genius.com.
    
    Takes a csv containing song title and artist information and attempts to scrape each record's 
    lyrics if available through a generic search on Genius's website. Truncates artist field to two words.
    Assumes columns named "Song" and "Artist" exist, and that the input is of csv format. As a 
    safety measure, splits lengthy arrays into arrays approx 500 records long, to save progress 
    periodically and reload the scraping browser between sections.
    """
    
    data_raw = pd.read_csv(document)

    artists = data_raw["Artist"].copy()

    # truncate artist field to 2 words
    for i in range(len(artists)):
        artists[i] = cutt(artists[i], 2)

    data_raw['artist_trunc'] = artists
    
    # define the search term to input on Genius' webpage
    data_raw["search_term"] = data_raw["Song"].map(str) + ' ' + data_raw["artist_trunc"].map(str)

    # split lengthy files into pieces
    if len(data_raw) > 600:
        collection = np.array_split(data_raw, len(data_raw)%400 + 1)
    else:
        collection = []
        collection.append(data_raw)

    iteration = 0

    # setting options for the browser
    options = webdriver.ChromeOptions()
    prefs = {
        "profile.managed_default_content_settings.images":2,
        "profile.managed_default_content_settings.javascript":1
    }
    options.add_experimental_option("prefs",prefs)
    
    
    for elem in collection:
        
        iteration += 1
        lyrics_raw = []
        
        # start the browser
        driver = webdriver.Chrome(Path2ChromeDriverEXE, chrome_options=options)
        driver.get('https://genius.com/Ed-sheeran-shape-of-you-lyrics')

        for i in elem['search_term']:

            lyrics_gotten = 0

            try:
                #wait only the amount of time necessary for the specified HTML element to appear
                element = WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/search-form/form/input"))
                )

                search = driver.find_element_by_xpath('/html/body/div[1]/search-form/form/input')
                
                # send search term to search box and submit
                search.send_keys(i)
                search.submit()

                element = WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]/search-result-items/div[1]/search-result-item/div/mini-song-card/a/div[2]'))
                    )
                
                # click the top recommended song link
                toplink = driver.find_element_by_xpath('/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]/search-result-items/div[1]/search-result-item/div/mini-song-card/a/div[2]')
                toplink.click()

                element = WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/routable-page/ng-outlet/song-page/div/div/div[2]/div[1]/div/defer-compile[1]/lyrics/div/section'))
                    )

                # grab lyrics
                lyrics = driver.find_element_by_xpath('/html/body/routable-page/ng-outlet/song-page/div/div/div[2]/div[1]/div/defer-compile[1]/lyrics/div/section')
                lyrics_text = lyrics.text

                # append lyrics to results
                lyrics_raw.append(lyrics_text)   
                lyrics_gotten = 1
        
            # not the best except clause but will do for now
            except:

                if lyrics_gotten == 0:
                    lyrics_raw.append("error")
                    os.system('say "there was a scraping error"')
                pass

        # place scraped lyrics into our dataframe for identification
        elem['lyrics_raw'] = lyrics_raw

        elem.to_csv(document[:-4] + "_lyrics_iteration_%d_marker.csv" % iteration, encoding='utf-8')

        # we quit and restart the browser every so often to clear the browser's cache and prevent hangups,
        # timeouts, and hopefully the throttling of suspicious activity
        driver.quit()

    # append all sections if necessary
    if len(collection) > 1:
		interesting_files = glob.glob("*.csv")
		df_list = []
		for filename in sorted(interesting_files):
		    df_list.append(pd.read_csv(filename))
		full_df = pd.concat(df_list)

		full_df.to_csv('output.csv')

