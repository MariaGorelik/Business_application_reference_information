from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    startDate = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(500), nullable=True)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artistId = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Time, nullable=False)
    releaseDate = db.Column(db.Date, nullable=False)
    rating = db.Column(db.Float, default=0)

    artist = db.relationship('Artist', backref=db.backref('songs', lazy=True))