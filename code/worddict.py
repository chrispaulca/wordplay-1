import csv
from tfidf import *
import sys
import boto3
from io import StringIO
import pandas as pd

# Global variables
id_lyric_map = {}
word_lyric_score_map = dict()
s3_bucket = 'wordplaydata'


def generate_word_lyric_score_map(word_score_tuple_list, song_id, the_map):
    """
    Given list of tuple (i.e. (word, score)) for a song and this song's id,
    add the corresponding information to a dictionary (or map) <the_map>.
    """
    for tuple in word_score_tuple_list:
        word = tuple[0]
        score = tuple[1]
        id_score_list = the_map.get(word)
        if id_score_list:
            id_score_list.append((song_id, score))
        else:  # originally empty
            the_map[word] = [(song_id, score)]
    return the_map


def sort_by_score(the_map):
    """
    In the constructed dictionary <word_lyric_score_map>, sort the tuples
    associated with each key word according to the tfidf scores in the
    tuples, so that the tuples (id, score) having the higher scores are in
    front of the dictionary value (i.e., the tuple list)
    """
    for key in the_map:
        the_id_score_list = the_map[key]
        the_id_score_list.sort(key=lambda tuple: tuple[1], reverse=True)
    return the_map


def find_song_by_word(word):
    """
    Given a key <word> provided by the caller, return the list of tuple
    (name, artist, album, lyric)
    """
    song_name_list = []
    tuple_list = word_lyric_score_map.get(word)
    if tuple_list:
        for tuple in tuple_list:
            song_name_list.append(id_lyric_map[tuple[0]])
    else:
        song_name_list = ['!!! Nothing Sorry !!!']
    return song_name_list


def init_dict():
    """
    Initialize the dictionary for later on searching.
    Load the csv raw source file from S3 and put the content into global
    variable <id_lyric_map> and construct the word dictionary
    <word_lyric_score_map> based on tfidf.
    """
    song_lyric_file = sys.argv[1]
    client = boto3.client('s3')
    obj = client.get_object(Bucket=s3_bucket, Key=song_lyric_file)
    body = obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string))
    for _, row in df.iterrows():
        id = row[0]
        name = row[1]
        artist = row[2]
        album = row[3]
        lyric = row[6]
        id_lyric_map[id] = (name, artist, album, lyric)

    tfidf = compute_tfidf(id_lyric_map)

    for key in id_lyric_map:
        tuple_list = summarize(tfidf, id_lyric_map[key][3])
        the_id = key
        generate_word_lyric_score_map(tuple_list, the_id, word_lyric_score_map)

    sort_by_score(word_lyric_score_map)

    # Save word_lyric_score_map to local csv file just for debugging purpose.
    with open('word_lyric_score_map.csv', 'w', newline='') as csvfile:
        fieldnames = ['word', 'maps']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in word_lyric_score_map:
            writer.writerow({'word': key, 'maps': word_lyric_score_map[key]})


# for testing this file only
if __name__ == '__main__':
    init_dict()
    ret_list = find_song_by_word(sys.argv[2])
    print(ret_list)
