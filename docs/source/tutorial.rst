WordPlay code tutorial
========================

Data collection: 

Go to code/scraping_code directory. Then run $python scrape_songs_wikipedia.py to scrape songs and run $python scrape_lyrics.py to scrape lyrics 

Algorithm:

Go to code directory. Run $python tfidf.py and $python worddict.py to generate 
{word:[(songID, TFIDF score), ... ]} and {word:[songID, ... ]} dictionaries. 


Server:

Run $python server.py in the code directory. 