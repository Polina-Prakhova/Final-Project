""" Description of Departments table """
import logging
import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(current_path, '..')
sys.path.append(ROOT_PATH)

# pylint: disable=wrong-import-position
from models import db
# pylint: enable=wrong-import-position

logger = logging.getLogger('department_app.run')


class Department(db.Model):
    """ Departments table. """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    avg_salary = db.Column(db.Float, nullable=False)
    count_employees = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(64))

    def __init__(self, name: str, email: str = ''):
        self.name = name
        self.email = email
        self.avg_salary = 0.0
        self.count_employees = 0
        logger.debug('Created Department instance. Department name is %s, '
                     'email = %s, average salary = %f, employees = %i',
                     self.name,
                     self.email,
                     self.avg_salary,
                     self.count_employees)

    # def __eq__(self, other):
    #     if not isinstance(other, Department):
    #         return NotImplemented
    #     return self.id == other.id\
    #            and self.name == other.name \
    #            and self.avg_salary == other.avg_salary \
    #            and self.count_employees == other.count_employees \
    #            and self.email == other.email

    def __repr__(self):
        return f'<Department {self.name}, {self.email}'
