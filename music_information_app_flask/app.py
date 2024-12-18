from flask import Flask, render_template, request, redirect, url_for
from orm_models import db, Artist, Song

app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://sa:486319@LAPTOP-1M8OJBHN\\SQLEXPRESS/Music_information?driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def index():
    dictionary = request.args.get('dictionary', 'artist')

    if dictionary == 'artist':
        artists = Artist.query.all()
        return render_template('index.html', dictionary=dictionary, artists=artists, songs=None)
    elif dictionary == 'song':
        songs = Song.query.all()
        artists = Artist.query.all()  # Для выпадающего списка с исполнителями
        return render_template('index.html', dictionary=dictionary, songs=songs, artists=artists)

    return render_template('index.html', dictionary=dictionary, artists=None, songs=None)


@app.route('/api/<entity>', methods=['POST'])
def add_record(entity):
    if entity == 'artist':
        name = request.form['name']
        startDate = request.form['startDate']
        country = request.form['country']
        description = request.form.get('description', '')
        artist = Artist(name=name, startDate=startDate, country=country, description=description)
        db.session.add(artist)
        db.session.commit()
        return redirect(url_for('index', dictionary='artist'))
    elif entity == 'song':
        artistId = request.form['artistId']
        title = request.form['title']
        genre = request.form['genre']
        duration = request.form['duration']
        releaseDate = request.form['releaseDate']
        rating = request.form['rating']
        song = Song(artistId=artistId, title=title, genre=genre, duration=duration, releaseDate=releaseDate,
                    rating=rating)
        db.session.add(song)
        db.session.commit()
        return redirect(url_for('index', dictionary='song'))
    return redirect(url_for('index'))


@app.route('/api/artist/delete/<int:artist_id>', methods=['GET'])
def delete_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if artist:
        db.session.delete(artist)
        db.session.commit()
    return redirect(url_for('index', dictionary='artist'))


@app.route('/api/song/delete/<int:song_id>', methods=['GET'])
def delete_song(song_id):
    song = Song.query.get(song_id)
    if song:
        db.session.delete(song)
        db.session.commit()
    return redirect(url_for('index', dictionary='song'))


@app.route('/api/artist/edit/<int:artist_id>', methods=['GET', 'POST'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if request.method == 'POST':
        artist.name = request.form['name']
        artist.startDate = request.form['startDate']
        artist.country = request.form['country']
        artist.description = request.form.get('description', '')
        db.session.commit()
        return redirect(url_for('index', dictionary='artist'))
    return render_template('edit_form.html', entity='artist', item=artist)


@app.route('/api/song/edit/<int:song_id>', methods=['GET', 'POST'])
def edit_song(song_id):
    song = Song.query.get(song_id)
    if request.method == 'POST':
        song.artistId = request.form['artistId']
        song.title = request.form['title']
        song.genre = request.form['genre']
        song.duration = request.form['duration']
        song.releaseDate = request.form['releaseDate']
        song.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('index', dictionary='song'))
    artists = Artist.query.all()
    return render_template('edit_form.html', entity='song', item=song, artists=artists)


if __name__ == '__main__':
    app.run(debug=True)
