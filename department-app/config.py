""" Database configuration data."""

DATABASE_USER = 'root'
DATABASE_PASSWORD = 'root'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'
DATABASE_NAME = 'project'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://' \
                          f'{DATABASE_USER}:{DATABASE_PASSWORD}@' \
                          f'{DATABASE_HOST}/{DATABASE_NAME}'
