
How to build a web application
==============================

stack: Flask + SQLAlchemy + PostgreSQL


### the MVC pattern

- **models**: the database manipulated through SQLAlchemy
- **views**: the HTML served through Flask + Jinja2
- **controllers**: Flask route functions telling models what to do and views what to display


### Steps

Here is an overview of the list of tasks we'll need to do for a given web app to run with a database.

1. Start from the database
    - Create a database using `createdb` in Postgres
    - Establish a connection to the database, add its URI to `config.py`
    - Create the table models and estabilish relationships among them
    - Create the database table running the migrations
    - Seed the database with initial data
1. Write the tests for the routes
1. Write the routes which can either serve as API or to display views
    - If a frontend is needed, write the HTML, CSS and Javascript for the views
    - Remeber: they must satisfy the tests!
1. **Run the app**: `FLASK_APP=app.py FLASK_DEBUG=true flask run`
1. setup the roles
1. Deploy the server to the web.
<br>
<br>
<br>
---
<br>
<br>
<br>

#### Project layout

This layout is automatically generated running `create_flask.sh` from `/media/alfx/LOCAL_data/code`

```
/home/user/Projects/flask-tutorial
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── venv/
├── setup.py
└── MANIFEST.in

```


#### Configuration

[source](https://hackersandslackers.com/configure-flask-applications/)

**`app/config.py`**
```python
import os


class Config:
    SECRET_KEY = os.urandom(32)             # used to encrypt sensitive user data
    DEBUG = True                            # verbose HTML traceback, app auto-reloads after crashing
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # remove useless messages

    user = 'postgres'
    pw = 'postgres'
    host = 'localhost'
    port = '5432'
    db = 'capstone'

    SQLALCHEMY_DATABASE_URI = f'postgres://{user}:{pw}@{host}:{port}/{db}'  # locates the database
```


#### Models

Regular model representing a data table in SQL

**`app/models.py`**
```python
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    genre = db.relationship('Genre', secondary=movie_genre, backref='movie')
    interpretation = db.relationship('Interpretation', back_populates='movie')

    # `db.relationship()` is a function that points to another class

    # `backref` makes a relationship 2-way declaring the same property on the other class involved.
    # hence, both of the following statements are legal:
    # `my_movie.genre` will return the genre of a movie
    # `my_genre.movie` will return the movies associated to that genre

    # `back_populates` works the same as `backref` except that it is not automatically mirrored on the other model and therefore has to be manually specified

    # `secondary` indicates the association table used by a relationship function


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    surname = db.Column(db.String(120))
    dob = db.Column(db.DateTime, default=datetime.utcnow())
    gender = db.Column(db.String(120))
    interpretation = db.relationship('Interpretation', back_populates='actor')


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
```

Associaton Table representing a m2m relationship

**`app/models.py`**
```python
movie_genre = db.Table(
        'movie_genre',
        db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
        db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'))
    )
```

Association Object representing a m2m relationship with additional fields

**`app/models.py`**
```python
class Interpretation(db.Model):
    __tablename__ = 'interpretations'
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey(Actor.id))
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id))
    character = db.Column(db.String(120))
    movie = db.relationship('Movie', back_populates='interpretation')
    actor = db.relationship('Actor', back_populates='interpretation')
```

#### App Factory

**`app/__init__.py`**
```python
from flask import Flask
from flask_migrate import Migrate
from app.models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/')
    def index():
        return "Hello World!"

    return app
```

Run with:
```bash
$ FLASK_APP=app FLASK_ENV=development flask run
```


#### Miscellanea

In the case of Project 1 (Fyyur), I need to write the backend to an existing website working on fake data. Hence I need "wire" the HTML to the views; search for the HTML tags, eg:

- to find the HTML element leading to the `/venues/search` endpoint:
    - search the endpoint through all the project files (`ctrl + shift + f`)
    - find the form element with the attribute `action="/venues/search"`
    - get the attribute `name="search_term"`
    - this enables you to retrieve the user input as follows:<br>
    `search_term = request.form.get('search_term', '').strip()`


- an HTML form returns a `request` object
    - [docs](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Request)
    - [question](https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request)
- its content can be accessed through `request.__dict__`
- input from a POST request from a form is accessed with `request.form`
