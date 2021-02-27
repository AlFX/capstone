import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from app.models import db, Movie, Actor


class ExecutiveTestCase(unittest.TestCase):
    ''' Test case for the Executive producer role which uses the JWT3 environment
    variable. Its permissions are as follows:

    - view actor
    - patch actor
    - add actor
    - delete actor

    - view movie
    - patch movie
    - add movie
    - delete movie

    '''

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

        self.test_actor = {
            'name': 'asd',
            'new_name': 'iop',
            'surname': 'qwe',
            'dob': '2000-01-01',
            'gender': 'male'
        }

        self.total_movies = 5
        self.total_actors = 6
        self.total_genres = 14
        self.jtw = os.getenv('AUTH0_JWT3')

    def tearDown(self):
        ''' Executed after each test function '''
        pass

    def test_index(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.decode('utf-8'),
                         '<h1>Welcome to Casting Agency API!</h1>')

    # ACTORS -----------------------------------------------------------

    def test_get_actor(self):
        res = self.client().get(
            '/actors/1',
            headers=[
                ('Content-Type', 'application/json'),
                ('Authorization', f'Bearer {self.jtw}')
            ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Humphrey')
        self.assertEqual(data['actor']['surname'], 'Bogart')

    def test_get_actor_not_found(self):
        res = self.client().get(
            '/actors/0',
            headers=[
                ('Content-Type', 'application/json'),
                ('Authorization', f'Bearer {self.jtw}')
            ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found.')

    def test_get_actors(self):
        res = self.client().get(
            '/actors',
            headers=[
                ('Content-Type', 'application/json'),
                ('Authorization', f'Bearer {self.jtw}')
            ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actor']), self.total_actors)

    def test_actor_1_add(self):
        res = self.client().post(
            f"/actors/add?name={self.test_actor['name']}&surname={self.test_actor['surname']}",
            headers=[
                ('Content-Type', 'application/json'),
                ('Authorization', f'Bearer {self.jtw}')
            ])
        data = json.loads(res.data)
        all_actors = Actor.query.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(all_actors), self.total_actors+1)

    def test_actor_2_update(self):
        # get the test actor from the database
        actor = Actor.query.filter_by(name=self.test_actor['name'].capitalize(),
                                      surname=self.test_actor['surname'].capitalize()).one_or_none()
        # update
        res = self.client().patch(
            f"/actors/update/{actor.id}?name={self.test_actor['new_name']}",
            headers=[
                ('Content-Type', 'application/json'),
                ('Authorization', f'Bearer {self.jtw}')
            ])
        data = json.loads(res.data)
        actor = Actor.query.get(actor.id)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], actor.id)
        # compare with lowercase because of automatic movie title
        # capitalization upon input, see capitalize_all() helper function
        self.assertEqual(actor.name.lower(), self.test_actor['new_name'])

    def test_actor_3_delete(self):
        actor = Actor.query.filter_by(name=self.test_actor['new_name'].capitalize(),
                                      surname=self.test_actor['surname'].capitalize()).one_or_none()
        res = self.client().delete(f"actors/delete/{actor.id}",
                                   headers=[
                                       ('Content-Type', 'application/json'),
                                       ('Authorization', f'Bearer {self.jtw}')
                                   ])
        data = json.loads(res.data)
        all_actors = Actor.query.all()
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor.id)
        self.assertEqual(len(all_actors), self.total_actors)

    def test_delete_actor_not_found(self):
        res = self.client().delete('/actors/delete/0',
                                   headers=[
                                       ('Content-Type', 'application/json'),
                                       ('Authorization', f'Bearer {self.jtw}')
                                   ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], 404)

    # MOVIES -----------------------------------------------------------

    def test_get_movie(self):
        res = self.client().get('/movies/1',
                                headers=[
                                    ('Content-Type', 'application/json'),
                                    ('Authorization', f'Bearer {self.jtw}')
                                ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'].lower(), 'casablanca')

    def test_get_movie_not_found(self):
        res = self.client().get('/movies/99',
                                headers=[
                                    ('Content-Type', 'application/json'),
                                    ('Authorization', f'Bearer {self.jtw}')
                                ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found.')

    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers=[
                                    ('Content-Type', 'application/json'),
                                    ('Authorization', f'Bearer {self.jtw}')
                                ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movie']), self.total_movies)

    def test_movie_1_add(self):
        # add
        res = self.client().post(
            f"/movies/add?title={self.test_movie['title']}",
            headers=[
                ('Content-Type', 'application/json'),
                ('Authorization', f'Bearer {self.jtw}')
            ])
        data = json.loads(res.data)
        # test addition
        all_movies = Movie.query.all()
        self.assertEqual(data['success'], True)
        self.assertEqual(len(all_movies), self.total_movies+1)

    def test_movie_2_update(self):
        # get the test movie from the database
        movie = Movie.query.filter_by(title=self.test_movie['title']
                                      .capitalize()).one_or_none()
        # update
        res = self.client().patch(
            f"/movies/update/{movie.id}?title={self.test_movie['new_title']}",
            headers=[
                ('Content-Type', 'application/json'),
                ('Authorization', f'Bearer {self.jtw}')
            ])
        data = json.loads(res.data)
        movie = Movie.query.get(movie.id)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], movie.id)
        # compare with lowercase because of automatic movie title
        # capitalization upon input, see capitalize_all() helper function
        self.assertEqual(movie.title.lower(), self.test_movie['new_title'])

    def test_movie_3_delete(self):
        # delete
        movie = Movie.query.filter_by(title=self.test_movie['new_title']
                                      .capitalize()).one_or_none()
        res = self.client().delete(f"/movies/delete/{movie.id}",
                                   headers=[
                                       ('Content-Type', 'application/json'),
                                       ('Authorization', f'Bearer {self.jtw}')
                                   ])
        data = json.loads(res.data)
        all_movies = Movie.query.all()
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie.id)
        self.assertEqual(len(all_movies), self.total_movies)

    def test_delete_movie_not_found(self):
        res = self.client().delete('/movies/delete/0',
                                   headers=[
                                       ('Content-Type', 'application/json'),
                                       ('Authorization', f'Bearer {self.jtw}')
                                   ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], 404)

    # GENRES -----------------------------------------------------------

    def test_get_genre(self):
        res = self.client().get('/genres/10',
                                headers=[
                                    ('Content-Type', 'application/json'),
                                    ('Authorization', f'Bearer {self.jtw}')
                                ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['genre']['name'].lower(), 'romance')

    def test_get_genre_not_found(self):
        res = self.client().get('/genres/99',
                                headers=[
                                    ('Content-Type', 'application/json'),
                                    ('Authorization', f'Bearer {self.jtw}')
                                ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found.')

    def test_get_genres(self):
        res = self.client().get('/genres',
                                headers=[
                                    ('Content-Type', 'application/json'),
                                    ('Authorization', f'Bearer {self.jtw}')
                                ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['genre']), self.total_genres)


if __name__ == '__main__':
    unittest.main()

# run with `python -m tests.tests`
