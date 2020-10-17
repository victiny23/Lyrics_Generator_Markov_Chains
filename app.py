from flask import Flask, render_template, request
from lyrics import scrape_lyrics_text
from markov import MarkovLyrics

app = Flask(__name__)


def generate_artist_lyrics(name):
    songs = scrape_lyrics_text(name)
    m = MarkovLyrics()
    for song in songs:
        m.populate_markov_chain(song)
    lyrics = m.generate_lyrics()
    return lyrics.split("NEWLINE")

@app.route('/', methods=['GET', 'POST'])
def lyrics_generator():
    lyrics = []
    if request.method == "POST":
        artist = request.form['search']
        lyrics = generate_artist_lyrics(artist)
    return render_template('home.html', lyrics=lyrics)

if __name__ == '__main__':
    app.run(debug=True)
