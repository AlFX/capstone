import os


class Config:
    """ Base config """

    # SECRET_KEY = environ.get('SECRET_KEY')
    SECRET_KEY = os.urandom(32)
    DEBUG = True
    username = "postgres"
    password = "postgres"
    host = "localhost"
    port = "5432"
    db_name = "capstone"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # TODO this wasn't working
    # def DATABASE_URI(self):
    #     SQLALCHEMY_DATABASE_URI = \
    #         f"postgres://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
    #     return SQLALCHEMY_DATABASE_URI

    SQLALCHEMY_DATABASE_URI = \
            f"postgres://{username}:{password}@{host}:{port}/{db_name}"
