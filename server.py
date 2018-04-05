import sys
from flask import Flask, render_template
import ast

word = 'khoury' # THIS WILL COME FROM THE USER SEARCH

app = Flask(__name__)

@app.route("/")
def search():

    return render_template('search.html')


@app.route("/?<word>")
def playlist(word):   
    
    # Display the playlist for a word/phrase
    with open("data/sample_output.txt", "r") as f:
        playlist = f.read()
        playlist = ast.literal_eval(playlist)

    return render_template('playlist.html', playlist=playlist, word=word)

app.run(host='0.0.0.0', port=80)
