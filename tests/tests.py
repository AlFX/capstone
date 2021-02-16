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

        self.test_movie = {
            'title': 'antani',
            'new_title': 'aruopolo',
            'release_date': '2000-01-01',
        }
        self.total_movies = 5
        self.total_actors = 6
        self.total_genres = 14

    def tearDown(self):
        ''' Executed after each test function '''
        pass

    def test_index(self):
        res = self.client().get('/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Welcome!')

    def test_get_actor(self):
        res = self.client().get('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Humphrey')
        self.assertEqual(data['actor']['surname'], 'Bogart')

    def test_get_actor_not_found(self):
        res = self.client().get('/actors/99')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found.')

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actor']), self.total_actors)

    def test_get_movie(self):
        res = self.client().get('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'].lower(), 'casablanca')

    def test_get_movie_not_found(self):
        res = self.client().get('/movies/99')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found.')

    def test_1_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movie']), self.total_movies)

    def test_get_genre(self):
        res = self.client().get('/genres/10')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['genre']['name'].lower(), 'romance')

    def test_get_genre_not_found(self):
        res = self.client().get('/genres/99')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found.')

    def test_get_genres(self):
        res = self.client().get('/genres')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['genre']), self.total_genres)

    def test_2_add_movie(self):
        # add
        res = self.client().post(f"/movies/add?title={self.test_movie['title']}")
        data = json.loads(res.data)
        # test addition
        all_movies = Movie.query.all()
        self.assertEqual(data['success'], True)
        self.assertEqual(len(all_movies), self.total_movies+1)

    def test_3_update_movie(self):
        # get the test movie from the database
        movie = Movie.query.filter_by(title=self.test_movie['title']
                                      .capitalize()).one_or_none()
        res = self.client()\
            .patch(f"/movies/update/{movie.id}?title={self.test_movie['new_title']}")
        data = json.loads(res.data)
        # update
        movie = Movie.query.get(movie.id)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], movie.id)
        # compare with lowercase because of automatic movie title
        # capitalization upon input, see capitalize_all() helper function
        self.assertEqual(movie.title.lower(), self.test_movie['new_title'])

    def test_4_delete_movie(self):
        # delete
        movie = Movie.query.filter_by(title=self.test_movie['new_title']
                                      .capitalize()).one_or_none()
        res = self.client().delete(f"/movies/delete/{movie.id}")
        data = json.loads(res.data)
        # update
        all_movies = Movie.query.all()
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie.id)
        self.assertEqual(len(all_movies), self.total_movies)

    def test_delete_movie_404(self):
        res = self.client().delete('/movies/delete/0')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], 404)


if __name__ == '__main__':
    unittest.main()

# run with `python -m tests.tests`
