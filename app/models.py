from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# simple m2m association table between Movie and Genre
movie_genre = db.Table(
    'movie_genre',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'))
    )


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    release_date = db.Column(db.DateTime, default=datetime.utcnow())
    genre = db.relationship('Genre', secondary=movie_genre, backref='movie')
    interpretation = db.relationship('Interpretation', back_populates='movie')

    def __repr__(self):
        return f"<{self.id}, {self.title}, {self.release_date}>"


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __repr__(self):
        return f"<{self.id}, {self.name}>"


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    surname = db.Column(db.String(120))
    dob = db.Column(db.DateTime, default=datetime.utcnow())
    gender = db.Column(db.String(10))
    interpretation = db.relationship('Interpretation', back_populates='actor')

    def __repr__(self):
        return f"<{self.id}, {self.name} {self.surname}, {self.dob}, {self.gender}>"


class Interpretation(db.Model):
    ''' complex m2m association object between Movie and Actor representing
    the role covered by an actor in a movie, the name of which is held
    by the "character" field '''
    __tablename__ = 'interpretations'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id))
    actor_id = db.Column(db.Integer, db.ForeignKey(Actor.id))
    character = db.Column(db.String(120))
    movie = db.relationship('Movie', back_populates='interpretation')
    actor = db.relationship('Actor', back_populates='interpretation')

    def __repr__(self):
        return f"<{self.id}, movie {self.movie_id}, actor {self.actor_id}, {self.character}>"
