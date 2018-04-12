WordPlay code tutorial
========================

Data collection: 

Run $scrape_songs_wikipedia.py in the code/scraping_code directory. Then
scrape lyrics with $scrape_lyrics.py .

Algorithm:

Run $tfidf.py in the code directory. Also run $worddict.py to generate 
{word:[(songID, TFIDF score), ... ]} and {word:[songID, ... ]} dictionaries. 


Server:
Run $server.py in the code directory. 