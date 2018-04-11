"""Scrapes songs from Wikipedia. Code towards end of file is from
https://github.com/rocheio/wiki-table-scrape/blob/master/wikitablescrape.py
"""

import csv
import os
import platform
import unidecode
import pandas as pd
import requests
from bs4 import BeautifulSoup

WIKI_BASE = 'https://en.wikipedia.org'


def songs_from_album(album_url):
    """Returns list of songs from Wikipedia album page
    ARGS:
        album_url (str): The full URL of the Wikipedia page to scrape from.
    """
    resp = requests.get(album_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    table_classes = {"class": "tracklist"}
    tracklist = soup.find("table", table_classes)
    songs = None
    if tracklist:
        songs = []
        for row in tracklist.findAll('tr',style=True):
            song = row.findAll('td')[1]
            if song.text:
                songs.append(song.text.strip('"'))
            elif song.find('a'):
                songs.append(song.find('a').text)
    else:
        tables = soup.findAll("ol")
        exclude = soup.findAll('ol',{'class':'references'})
        tracklist = set(tables).difference(exclude)
        if tracklist:
            songs = []
            for t in tracklist:
                for row in t.findAll('li'):
                    if row.find('ul'):
                        song = row.text.strip('"').split('"')[0]
                        songs.append(song)
    return songs


def songs_from_artists_albums(albums, artists, album_urls, folder_name=None):
    """Create dataframe of all songs in a list of albums in a year 
    ARGS:
    albums_url (str): The URL of the Wikipedia article to scrape from.
    """
    SONGS = [] 
    if folder_name is None:
        folder_name = './'
    for i,a in enumerate(album_urls):
        songs = songs_from_album(a)
        if songs is None:
            print(i)
        else:
            SONGS.append(songs)

    final_songs = []
    for i in range(len(artists)):
        ar = artists[i]
        al = albums[i]
        final_songs.extend(list((s, ar, al) for s in SONGS[i]))

    df = pd.DataFrame(final_songs, columns = ['Song', 'Artist','Album'])
    return df
#     df.to_csv('{}.csv'.format(output_dir), index=False) 


def scrape_billboards(start_url,search_str):
    """Returns list of Billboard links (one for each year)
    ARGS:
    start_url (str): The URL of the Wikipedia article to scrape tables from.
    search_str (str): The title of the table with the series of years
    """
    # get links for Billboard 200 singles for each year (1959-2018)
    resp = requests.get(start_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    links = soup.findAll('a',href=True,title=True)
    billboards = [l['href'] for l in links if search_str in l['title']]
    billboards = ['https://en.wikipedia.org' + b for b in billboards]
    billboards.append(start_url)
    return billboards

    # folder_name = search_str.replace(' ','_')
    # if singles:
    #     for b in billboards:
    #         scrape_singles(b, folder_name)
    # else:
    #     for b in billboards:
    #         scrape_albums(b, folder_name)
    

def scrape_albums_1956_2013(url):
    """Returns lists of albums and artists for Billboards that year (1956-2013)
    ARGS:
    url (str): The URL of the Wikipedia article to scrape from.
    """
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")

    table_classes = {"class": "wikitable"}
    tables = soup.findAll('table', table_classes)  # find the table
    if len(tables) > 1:
        table = [t for t in tables if len(t.findAll('td'))>2][0]

    albums = []
    album_urls = []
    artists = []
    for row in table.findAll('tr')[1:]: #excluding header row
        albuminfo = row.findAll('td')
        if len(albuminfo) > 2:
            if albuminfo[1].find('a'): #if album has link to its songs
                albums.append(albuminfo[1].text)
                album_urls.append(WIKI_BASE + albuminfo[1].find('a')['href'])
                artists.append(albuminfo[2].text)
    return albums, artists, album_urls


def scrape_albums_2014_2017(url):
    """Returns lists of albums and artists for Billboards that year (2014-2017)
    ARGS:
    url (str): The URL of the Wikipedia article to scrape from.
    """
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    table_classes = {"class": ["sortable", "plainrowheaders"]}
    table = soup.find('table', table_classes)  # find the table
    if table is None:
        print(url)
        return
    albums = []
    album_urls = []
    artists = []
    # creates lists of artists and albums in table
    for row in table.findAll('tr')[1:]: #excluding header row
        if len(row.findAll('a',title=True)) == 2: #if artist has link
            album = row.findAll(['td','a'])[0]
            if album.find('a') and 'reference' not in str(album):
                album_urls.append(WIKI_BASE + album.find('a')['href'])
                albums.append(album.text)
            artist = row.findAll('td')[1]
            if artist.find('a', title=True):
                artists.append(artist.find('a').text)
    return albums, artists, album_urls


def get_songs_year(albums, artists, album_urls, folder_name):
    """Create dataframe of all songs in a list of albums in a year 
    ARGS:
    albums_url (str): The URL of the Wikipedia article to scrape from.
    """

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # creates list of tracklists
    SONGS = [] 
    for i,a in enumerate(albums):
        songs = songs_from_album(a)
        if songs is None:
            print(i)
        else:
            SONGS.append(songs)

    if len(SONGS) != len(artists):
        print(url)
        return

    final_songs = []
    for i in range(len(artists)):
        a = artists[i]
        final_songs.extend(list((s, a) for s in SONGS[i]))

    output_dir = os.path.join(folder_name,output_name)

    df = pd.DataFrame(final_songs, columns = ['Song', 'Artist'])
    df.to_csv('{}.csv'.format(output_dir), index=False)

    # combines all the songs
    songs_list = glob.glob(os.path.join(folder_name, "*.csv"))
    df = pd.concat([pd.read_csv(f) for f in songs_list])
    df.to_csv('{}.csv'.format(folder_name), index=False)


def scrape_singles(url, folder_name=None):
    """Create CSVs from all tables in a Wikipedia article.
    ARGS:
        url (str): The full URL of the Wikipedia article to scrape tables from.
        output_name (str): The base file name (without filepath) to write to.
    """

    # Read tables from Wikipedia article into list of HTML strings
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    table_classes = {"class": ["sortable", "plainrowheaders"]}
    wikitables = soup.findAll("table", table_classes)
    output_name = os.path.split(url)[1]

    if folder_name is None:
        folder_name = output_name
    # write data out
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for index, table in enumerate(wikitables):
        # Make a unique file name for each CSV
        if index == 0:
            filename = output_name
        else:
            filename = output_name + '_' + str(index)

        filepath = os.path.join(folder_name, filename) + '.csv'

        with open(filepath, mode='w', newline='', encoding='utf-8') as output:
            # Deal with Windows inserting an extra '\r' in line terminators
            csv_writer = csv.writer(output, quoting=csv.QUOTE_ALL)

            write_html_table_to_csv(table, csv_writer)

    # combines all the songs
    songs_list = glob.glob(os.path.join(folder_name, "*.csv"))
    df = pd.concat([pd.read_csv(f) for f in songs_list])
    df = df[['Title', 'Artist(s)']]
    df.rename(columns={'Title':'Song', 'Artist(s)':'Artist'}, inplace=True)
    df['Song'] = df['Song'].str.strip('"')
    df.to_csv('{}.csv'.format(folder_name), index=False)


def write_html_table_to_csv(table, writer):
    """Write HTML table from Wikipedia to a CSV file.
    ARGS:
        table (bs4.Tag): The bs4 Tag object being analyzed.
        writer (csv.writer): The csv Writer object creating the output.
    """

    # Hold elements that span multiple rows in a list of
    # dictionaries that track 'rows_left' and 'value'
    saved_rowspans = []
    for row in table.findAll("tr"):
        cells = row.findAll(["th", "td"])

        # If the first row, use it to define width of table
        if len(saved_rowspans) == 0:
            saved_rowspans = [None for _ in cells]
        # Insert values from cells that span into this row
        elif len(cells) != len(saved_rowspans):
            for index, rowspan_data in enumerate(saved_rowspans):
                if rowspan_data is not None:
                    # Insert the data from previous row; decrement rows left
                    value = rowspan_data['value']
                    cells.insert(index, value)

                    if saved_rowspans[index]['rows_left'] == 1:
                        saved_rowspans[index] = None
                    else:
                        saved_rowspans[index]['rows_left'] -= 1

        # If an element with rowspan, save it for future cells
        for index, cell in enumerate(cells):
            if cell.has_attr("rowspan"):
                rowspan_data = {
                    'rows_left': int(cell["rowspan"]),
                    'value': cell,
                }
                saved_rowspans[index] = rowspan_data

        if cells:
            # Clean the data of references and unusual whitespace
            cleaned = clean_data(cells)

            # Fill the row with empty columns if some are missing
            # (Some HTML tables leave final empty cells without a <td> tag)
            columns_missing = len(saved_rowspans) - len(cleaned)
            if columns_missing:
                cleaned += [None] * columns_missing

            writer.writerow(cleaned)


def clean_data(row):
    """Clean table row list from Wikipedia into a string for CSV.
    ARGS:
        row (bs4.ResultSet): The bs4 result set being cleaned for output.
    RETURNS:
        cleaned_cells (list[str]): List of cleaned text items in this row.
    """

    cleaned_cells = []

    for cell in row:
        # Strip references from the cell
        references = cell.findAll("sup", {"class": "reference"})
        if references:
            for ref in references:
                ref.extract()

        # Strip sortkeys from the cell
        sortkeys = cell.findAll("span", {"class": "sortkey"})
        if sortkeys:
            for ref in sortkeys:
                ref.extract()

        # Strip footnotes from text and join into a single string
        text_items = cell.findAll(text=True)
        no_footnotes = [text for text in text_items if text[0] != '[']

        cleaned = (
            ''.join(no_footnotes)  # Combine elements into single string
            .replace('\xa0', ' ')  # Replace non-breaking spaces
            .replace('\n', ' ')  # Replace newlines
            .strip()
        )

        cleaned = unidecode.unidecode(cleaned)
        cleaned_cells += [cleaned]

    return cleaned_cells

if __name__ == '__main__':
    url = WIKI_BASE + '/wiki/List_of_Billboard_200_number-one_albums_of_2017'
    search_str = 'List of Billboard 200 number-one albums of'
    scrape_billboards(url,search_str)

