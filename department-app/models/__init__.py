""" Creating SQLAlchemy instance to work with database. """
import logging

from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger('department_app.run')

db = SQLAlchemy()
logger.debug('Created SQLAlchemy instance.')
