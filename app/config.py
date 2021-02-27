import os


class Config:
    ''' Base config '''

    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    username = 'postgres'
    password = 'postgres'
    host = 'localhost'
    port = '5432'
    db_name = 'capstone'

    SQLALCHEMY_DATABASE_URI = \
        f"postgresql://{username}:{password}@{host}:{port}/{db_name}"


class Production(Config):
    ''' Config for Heroku production environment '''

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
