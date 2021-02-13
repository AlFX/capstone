import colored_traceback.auto
from app.models import db, Movie, Genre, Actor, Interpretation, movie_genre
from dummy_data import (movies, genres, actors, interpretations,
                        movie_genre_association)
from app.__init__ import create_app


def populate_movies(to_add=movies):
    i = 0
    for item in to_add:
        if not (Movie.query.filter_by(title=item.get('title')).first()):
            i += 1
            movie = Movie(
                id=item.get('id'),
                title=item.get('title'),
                release_date=item.get('release_date')
            )
            db.session.add(movie)
    db.session.commit()
    print(f'\n>>> Movies input complete with {i} items.')


def populate_genres(to_add=genres):
    i = 0
    for name, genre_id in to_add.items():
        if not (Genre.query.filter_by(name=name).first()):
            i += 1
            genre = Genre(
                id=genre_id,
                name=name
            )
            db.session.add(genre)
    db.session.commit()
    print(f'\n>>> Genres input complete with {i} items.')


def populate_actors(to_add=actors):
    i = 0
    for item in to_add:
        if not (Actor.query.filter_by(surname=item.get('surname')).first()):
            i += 1
            actor = Actor(
                id=item.get('id'),
                name=item.get('name'),
                surname=item.get('surname'),
                dob=item.get('dob'),
                gender=item.get('gender')
            )
            db.session.add(actor)
    db.session.commit()
    print(f'\n>>> Actors input complete with {i} items.')


def populate_interpretations(to_add=interpretations):
    i = 0
    for item in to_add:
        if not (Interpretation.query.filter_by(character=item.get('character'))
                .first()):
            i += 1
            interpretation = Interpretation(
                movie_id=item.get('movie_id'),
                actor_id=item.get('actor_id'),
                character=item.get('character'),
            )
            db.session.add(interpretation)
    db.session.commit()
    print(f'\n>>> Interpretations input complete with {i} items.')


def populate_movie_genre(to_add=movie_genre_association):
    i = 0
    for item in to_add:
        i += 1
        stmt = movie_genre.insert().values(
            movie_id=item.get('movie_id'),
            genre_id=item.get('genre_id'),
        )
        db.session.execute(stmt)
    db.session.commit()
    print(f'\n>>> Movies & Genres input complete with {i} items.')


if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    populate_movies()
    populate_genres()
    populate_actors()
    populate_interpretations()
    populate_movie_genre()
