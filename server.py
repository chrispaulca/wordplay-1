import sys
from flask import Flask, render_template
import ast
import forms

word = 'khoury' # THIS WILL COME FROM THE USER SEARCH

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return playlist(search)

    return render_template('search.html', form=search)


@app.route("/results")
def playlist(search):

    print search

    # Display the playlist for a word/phrase
    with open("data/sample_output.txt", "r") as f:
        playlist = f.read()
        playlist = ast.literal_eval(playlist)

    return render_template('playlist.html', playlist=playlist, word=word)

app.run(host='0.0.0.0', port=80)
