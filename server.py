import sys
from flask import Flask, render_template, request
import ast
from forms import SearchForm

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return playlist(search)

    return render_template('search.html', form=search)


@app.route("/results")
def playlist(search):

    # Display the playlist for a word/phrase
    with open("data/sample_output.txt", "r") as f:
        playlist = f.read()
        playlist = ast.literal_eval(playlist)

    return render_template('playlist.html', playlist=playlist, word=search.data['search'])

app.run(host='0.0.0.0', port=80)
