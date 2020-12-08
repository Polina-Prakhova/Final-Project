""" Database configuration data."""


class Config:
    """ Main configuration class with main parameters. """
    DEBUG = False
    TESTING = False

    SECRET_KEY = 'very_secret'

    DATABASE_USER = 'root'
    DATABASE_PASSWORD = 'root'
    DATABASE_HOST = 'localhost'
    DATABASE_NAME = 'development_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE = f'mysql+mysqlconnector://' \
                        f'{DATABASE_USER}:{DATABASE_PASSWORD}@' \
                        f'{DATABASE_HOST}'
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://' \
                              f'{DATABASE_USER}:{DATABASE_PASSWORD}@' \
                              f'{DATABASE_HOST}/{DATABASE_NAME}'


class DevelopmentConfig(Config):
    """ Configuration class for development. """
    DEBUG = True
    DATABASE_NAME = 'development_db'


class TestingConfig(Config):
    """ Configuration class for testing. """
    TESTING = True
    DATABASE_NAME = 'testing_db'
