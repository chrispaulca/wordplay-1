"""
This is the flask code for the webpage
"""

from flask import Flask, render_template, request
from forms import SearchForm
from worddict import *

app = Flask(__name__)
init_dict()


@app.route("/", methods=['GET', 'POST'])
def index():
    """
    Represents the landing page with a search bar.  Returns a playlist if
    the user submits a post request
    """
    search = SearchForm(request.form)
    if request.method == 'POST':
        return playlist(search)

    return render_template('search.html', form=search)


@app.route("/results")
def playlist(search):
    """
    Reads in the playlist information and displays to the user
    """
    playlist = find_song_by_word(search.data['search'])
    print(playlist)
    return render_template('playlist.html', playlist=playlist,
                           word=search.data['search'])


app.run(host='0.0.0.0', port=80)
