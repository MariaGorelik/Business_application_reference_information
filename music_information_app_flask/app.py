from flask import Flask, render_template, request, redirect, url_for
from orm_models import db, Artist, Song

app = Flask(__name__)

# Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://sa:486319@LAPTOP-1M8OJBHN\\SQLEXPRESS/Music_information?driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications

# Initialize the SQLAlchemy object
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

# API route for loading Artist data
@app.route('/api/artist', methods=['GET'])
def get_artists():
    artists = Artist.query.all()  # Get all artists from the database
    fields = ['id', 'name', 'startDate', 'country', 'description']  # Fields to display
    return render_template('table.html', data=artists, fields=fields, getattr=getattr, entity="artist")

# API route for loading Song data
@app.route('/api/song', methods=['GET'])
def get_songs():
    songs = Song.query.all()  # Получаем все песни из базы данных
    fields = ['id', 'artist.name', 'title', 'genre', 'duration', 'releaseDate', 'rating']  # Добавляем поле для имени исполнителя
    artists = Artist.query.all()  # Получаем всех исполнителей
    return render_template('table.html', data=songs, fields=fields, getattr=getattr, entity="song", artists=artists)


# API route for adding an Artist entry
@app.route('/api/<entity>', methods=['POST'])
def add_record(entity):
    if entity == 'artist':
        name = request.form['name']
        startDate = request.form['startDate']
        country = request.form['country']
        description = request.form.get('description', '')

        # Создание нового исполнителя и добавление его в базу данных
        artist = Artist(name=name, startDate=startDate, country=country, description=description)
        db.session.add(artist)
        db.session.commit()

        return redirect(url_for('get_artists'))

    elif entity == 'song':
        artistId = request.form['artistId']
        title = request.form['title']
        genre = request.form['genre']
        duration = request.form['duration']
        releaseDate = request.form['releaseDate']
        rating = request.form['rating']

        # Создание новой песни и добавление в базу данных
        song = Song(artistId=artistId, title=title, genre=genre, duration=duration, releaseDate=releaseDate,
                    rating=rating)
        db.session.add(song)
        db.session.commit()

        return redirect(url_for('get_songs'))

    return redirect(url_for('index'))  # На случай, если не передан правильный entity


# API route for deleting an Artist entry
@app.route('/api/artist/delete/<int:artist_id>', methods=['GET'])
def delete_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if artist:
        db.session.delete(artist)
        db.session.commit()
    return redirect(url_for('get_artists'))

# API route for deleting a Song entry
@app.route('/api/song/delete/<int:song_id>', methods=['GET'])
def delete_song(song_id):
    song = Song.query.get(song_id)
    if song:
        db.session.delete(song)
        db.session.commit()
    return redirect(url_for('get_songs'))

# API route for editing an Artist entry
@app.route('/api/artist/edit/<int:artist_id>', methods=['GET', 'POST'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if request.method == 'POST':
        artist.name = request.form['name']
        artist.startDate = request.form['startDate']
        artist.country = request.form['country']
        artist.description = request.form.get('description', '')
        db.session.commit()
        return redirect(url_for('get_artists'))
    return render_template('edit_form.html', entity='artist', item=artist)

# API route for editing a Song entry
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
        return redirect(url_for('get_songs'))
    artists = Artist.query.all()
    return render_template('edit_form.html', entity='song', item=song, artists=artists)

if __name__ == '__main__':
    app.run(debug=True)
