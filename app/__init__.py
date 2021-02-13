import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from app.models import db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)
    migrate = Migrate(app, db)
    # CORS(app)

    @app.route('/')
    def index():
        return "ok."

    return app

# how to run:
    # cd to the capstone/ directory
    # make sure the app is contained in an app sub-directory
    # $ FLASK_APP=app FLASK_ENV=development flask run
