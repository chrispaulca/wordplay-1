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


<<<<<<< HEAD
@app.route("/?<word>")
def playlist(word):   
    
=======
@app.route("/results")
def playlist(search):

>>>>>>> fb45f93b47a22bc68dcbdd4f300f7e7c39de28f4
    # Display the playlist for a word/phrase
    with open("data/sample_output.txt", "r") as f:
        playlist = f.read()
        playlist = ast.literal_eval(playlist)

    return render_template('playlist.html', playlist=playlist, word=search.data['search'])

app.run(host='0.0.0.0', port=80)
