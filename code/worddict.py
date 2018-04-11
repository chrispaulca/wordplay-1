import csv
from tfidf import *
from flask import Flask, render_template
import sys
import os

id_lyric_map = {}
word_lyric_score_map = dict()

def generate_word_lyric_score_map(word_score_tuple_list, song_id, the_map):
    for tuple in word_score_tuple_list:
        word = tuple[0]
        score = tuple[1]
        id_score_list = the_map.get(word)
        if id_score_list:
            id_score_list.append((song_id, score))
        else: # originally empty
            the_map[word] = [(song_id, score)]
    return the_map

def sort_by_score(the_map):
    for key in the_map:
        the_id_score_list = the_map[key]
        the_id_score_list.sort(key = lambda tuple: tuple[1], reverse=True) # sort by score.
    return the_map

def find_song_by_word(word):
    song_name_list = []
    tuple_list = word_lyric_score_map.get(word)
    if tuple_list:
        for tuple in tuple_list:
            song_name_list.append(id_lyric_map[tuple[0]][0])
    else:
        song_name_list = [ ' !!! Nothing Sorry !!!' ]
    return song_name_list


def init_dict():
    song_lyric_file = sys.argv[1]
    with open(song_lyric_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            id = row[0]
            name = row[1]
            artist = row[2]
            album = row[3]
            lyric = row[6]
            id_lyric_map[id] = (name, artist, album, lyric)

    # remove the header, because we assume there is a hearder
    # there is some other smarter way to detect if there is a header in the csv file
    # so that we can delete it smartly
    del id_lyric_map['']

    corpus = id_lyric_map
    tfidf = compute_tfidf(corpus)


    for key in corpus:
        tuple_list = summarize(tfidf, corpus[key][3])
        the_id = key
        generate_word_lyric_score_map(tuple_list, the_id, word_lyric_score_map)

    sort_by_score(word_lyric_score_map)

    with open('data/word_lyric_score_map.csv', 'w', newline='') as csvfile:
        fieldnames = ['word', 'maps']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in word_lyric_score_map:
            writer.writerow({'word': key, 'maps': word_lyric_score_map[key]})

