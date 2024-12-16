from flask_sqlalchemy import SQLAlchemy

# Create the db object separately
db = SQLAlchemy()

# Define the Artist model
class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    startDate = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(500), nullable=True)

# Define the Song model
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artistId = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Time, nullable=False)
    releaseDate = db.Column(db.Date, nullable=False)
    rating = db.Column(db.Float, default=0)

# Define the Dictionary model
class Dictionary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    displayName = db.Column(db.String(100), nullable=False)

# Define the DictionaryFields model
class DictionaryFields(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dictionaryId = db.Column(db.Integer, db.ForeignKey('dictionary.id'), nullable=False)
    fieldName = db.Column(db.String(100), nullable=False)
    displayName = db.Column(db.String(100), nullable=False)
    fieldType = db.Column(db.String(20), nullable=False)
