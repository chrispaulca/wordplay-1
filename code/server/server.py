"""
This is the flask code for the webpage
"""

from flask import Flask, render_template, request
from forms import SearchForm
import sys
sys.path.insert(0, '../algorithms/')
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
    playlist = find_song_by_word(search.data['search'].lower())
    return render_template('playlist.html', playlist=playlist,
                           word=search.data['search'])

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 80
    try:
        app.run(host=host, port=port)
    except:
        print('failed to launch at {}:{}'.format(host,port))
