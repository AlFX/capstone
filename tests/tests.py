import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from app.models import db, Movie, Actor


class BasicTestCase(unittest.TestCase):
    ''' Most basic test possible '''

    def setUp(self):
        ''' Executed before each test function '''
        self.app = create_app()
        self.client = self.app.test_client
        self.user = 'postgres'
        self.pw = 'postgres'
        self.host = 'localhost'
        self.port = '5432'
        self.db_name = 'capstone'
        self.database_path = \
            f'postgresql://{self.user}:{self.pw}@{self.host}:{self.port}/{self.db_name}'

        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = self.app
        db.init_app(self.app)
        db.create_all()

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        ''' Executed after each test function '''
        pass

    def test_index(self):
        res = self.client().get('/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Welcome!')

    def test_actor(self):
        res = self.client().get('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], 'Humphrey Bogart')

    def test_actor_not_found(self):
        res = self.client().get('/actors/99')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found.')

    def test_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actor']), 6)

    def test_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movie']), 5)


    # TODO tests
    # Two GET requests
        # search actor > movies + characters
        # search movie > genre, actors + characters
        # search genre > movies
    # One POST request > add movie
    # One PATCH request > edit movie
    # One DELETE request > delete movie


if __name__ == '__main__':
    unittest.main()

# run with `python -m tests.tests`
