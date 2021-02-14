import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from app.models import db, Actor, Movie


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)
    migrate = Migrate(app, db)
    # CORS(app)

    # ROUTES
    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'Welcome!'
            })

    @app.route('/actors/<int:actor_id>')
    def actor(actor_id):
        try:
            actor = Actor.query.get(actor_id)
            return jsonify({
                'success': True,
                'actor': actor.name + ' ' + actor.surname,
                })
        except AttributeError:  # happens when actor is None
            abort(404)
        except Exception:
            abort(422)

    @app.route('/actors')
    def actors():
        try:
            actors = Actor.query.all()
            actors = [f"{actor.name} {actor.surname}" for actor in actors]
            return jsonify({
                'success': True,
                'actor': actors
                })
        except Exception as e:
            raise e

    @app.route('/movies')
    def movies():
        try:
            movies = Movie.query.all()
            movies = [movie.title for movie in movies]
            return jsonify({
                'success': True,
                'movie': movies
                })
        except Exception as e:
            raise e


    # ERROR HANDLERS
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request.'
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

    return app

# how to run:
    # cd to the capstone/ directory
    # make sure the app is contained in an app sub-directory
    # $ FLASK_APP=app FLASK_ENV=development flask run
