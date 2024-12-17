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
    return render_template('table.html', data=artists, fields=fields, getattr=getattr)

# API route for loading Song data
@app.route('/api/song', methods=['GET'])
def get_songs():
    songs = Song.query.all()  # Получаем все песни из базы данных
    fields = ['id', 'artist.name', 'title', 'genre', 'duration', 'releaseDate', 'rating']  # Добавляем поле для имени исполнителя
    return render_template('table.html', data=songs, fields=fields, getattr=getattr)

# API route for adding an Artist entry
@app.route('/api/artist', methods=['POST'])
def add_artist():
    name = request.form['name']
    startDate = request.form['startDate']
    country = request.form['country']
    description = request.form.get('description', '')

    # Create new Artist object and add it to the database
    artist = Artist(name=name, startDate=startDate, country=country, description=description)
    db.session.add(artist)
    db.session.commit()

    return redirect(url_for('get_artists'))

# API route for adding a Song entry
@app.route('/api/song', methods=['POST'])
def add_song():
    artistId = request.form['artistId']
    title = request.form['title']
    genre = request.form['genre']
    duration = request.form['duration']
    releaseDate = request.form['releaseDate']
    rating = request.form['rating']

    # Создание новой песни и добавление в базу данных
    song = Song(artistId=artistId, title=title, genre=genre, duration=duration, releaseDate=releaseDate, rating=rating)
    db.session.add(song)
    db.session.commit()

    return redirect(url_for('get_songs'))


@app.route('/add_song', methods=['GET'])
def add_song_form():
    artists = Artist.query.all()  # Получаем всех исполнителей
    return render_template('add_song.html', artists=artists)


if __name__ == '__main__':
    app.run(debug=True)
