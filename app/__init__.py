import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_cors import CORS

from app.models import db, Actor, Movie, Genre
from app.auth import requires_auth, get_token_auth_header, AuthError


# APP FACTORY ----------------------------------------------------------
def create_app(production=False):
    # create and configure the app
    app = Flask(__name__)
    if production:
        app.config.from_object('app.config.Production')
    else:
        app.config.from_object('app.config.Config')
    db.init_app(app)
    migrate = Migrate(app, db)
    # CORS(app)

# ROUTES ---------------------------------------------------------------

    @app.route('/')
    def index():
        # return jsonify({
        #     'success': True,
        #     'message': 'Welcome!'
        # })
        return '<h1>Welcome to Casting Agency API!</h1>'

    @app.route('/login-results')
    def loggedin():
        return '<h1>Please copy the JWT</h1>'

    # MOVIES -----------------------------------------------------------

    @app.route('/movies/<int:movie_id>')
    @requires_auth(permission='get:movies')
    def movie(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)
            return jsonify({
                'success': True,
                'movie': movie.format(),
            })
        except AttributeError:  # happens when movie is None
            abort(404)
        except Exception:
            abort(422)

    @app.route('/movies')
    @requires_auth(permission='get:movies')
    def movies(payload):
        try:
            movies = Movie.query.all()
            movies = [movie.format() for movie in movies]
            return jsonify({
                'success': True,
                'movie': movies
            })
        except AttributeError:
            abort(404)
        except Exception:
            abort(422)

    @app.route('/movies/add', methods=['POST'])
    @requires_auth(permission='post:movies')
    def add_movie(payload):
        try:
            title = capitalize_all(request.args.get('title'))
            if not title:
                abort(400)
            release_date = request.args.get('release_date')
            new_movie = Movie(
                title=title,
                release_date=release_date,
            )
            new_movie.insert()
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'added': new_movie.id
        })

    @app.route('/movies/update/<int:movie_id>', methods=['PATCH'])
    @requires_auth(permission='patch:movies')
    def update_movie(payload, movie_id):
        try:
            # get the object from id
            movie = Movie.query.get(movie_id)
            if not movie:
                abort(404)
            title = capitalize_all(request.args.get('title'))
            release_date = request.args.get('release_date')
            # update the object
            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date
            movie.update()
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'updated': movie.id
        })

    @app.route('/movies/delete/<int:movie_id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)
            movie.delete()
        except AttributeError:
            abort(404)
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'deleted': movie.id
        })

    # GENRES -----------------------------------------------------------

    @app.route('/genres/<int:genre_id>')
    @requires_auth(permission='get:movies')
    def genre(payload, genre_id):
        try:
            genre = Genre.query.get(genre_id)
            return jsonify({
                'success': True,
                'genre': genre.format(),
            })
        except AttributeError:  # happens when genre is None
            abort(404)
        except Exception:
            abort(422)

    @app.route('/genres')
    @requires_auth(permission='get:movies')
    def genres(payload):
        try:
            genres = Genre.query.all()
            genres = [genre.format() for genre in genres]
            return jsonify({
                'success': True,
                'genre': genres
            })
        except AttributeError:
            abort(404)
        except Exception:
            abort(422)

    # ACTORS -----------------------------------------------------------

    @app.route('/actors/<int:actor_id>')
    @requires_auth(permission='get:actors')
    def actor(payload, actor_id):
        ''' get the actors full list '''
        try:
            actor = Actor.query.get(actor_id)
            return jsonify({
                'success': True,
                'actor': actor.format(),
            })
        except AttributeError:  # happens when actor is None
            abort(404)
        except Exception:
            abort(422)

    @app.route('/actors')
    @requires_auth(permission='get:actors')
    def actors(payload):
        try:
            actors = Actor.query.all()
            actors = [actor.format() for actor in actors]
            return jsonify({
                'success': True,
                'actor': actors
            })
        except AttributeError:
            abort(404)
        except Exception:
            abort(422)

    @app.route('/actors/add', methods=['POST'])
    @requires_auth(permission='post:actors')
    def add_actor(payload):
        try:
            name = request.args.get('name').capitalize()
            surname = request.args.get('surname').capitalize()
            if (not name) or (not surname):
                abort(400)
            new_actor = Actor(
                name=name,
                surname=surname,
            )
            new_actor.insert()
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'added': new_actor.id
        })

    @app.route('/actors/update/<int:actor_id>', methods=['PATCH'])
    @requires_auth(permission='patch:actors')
    def update_actor(payload, actor_id):
        try:
            # get the object from id
            actor = Actor.query.get(actor_id)
            if not actor:
                abort(404)
            name = request.args.get('name')
            surname = request.args.get('surname')
            # update the object
            if name:
                actor.name = name.capitalize()
            if surname:
                actor.surname = surname.capitalize()
            actor.update()
        except Exception as e:
            # abort(422)
            raise e

        return jsonify({
            'success': True,
            'updated': actor.id
        })

    @app.route('/actors/delete/<int:actor_id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)
            actor.delete()
        except AttributeError:
            abort(404)
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'deleted': actor.id
        })

    # ERROR HANDLERS ---------------------------------------------------
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request.'
        })

    @app.errorhandler(AuthError)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized.'
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found.'
        })

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        })

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        })

    # HELPER FUNCTIONS -------------------------------------------------
    def capitalize_all(words):
        ''' Capitalize a string made of multiple words '''
        words = words.split(' ')
        words = ' '.join([x.capitalize() for x in words])
        return words

    return app

# how to run:
    # cd to the capstone/ directory
    # make sure the app is contained in an app sub-directory
    # $ FLASK_APP=app FLASK_ENV=development flask run
