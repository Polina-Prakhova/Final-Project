""" Description of Employees table """
import logging
from datetime import date
import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(current_path, '..')
sys.path.append(ROOT_PATH)

# pylint: disable=wrong-import-position
from models.department_model import Department
from models import db
# pylint: enable=wrong-import-position

logger = logging.getLogger('department_app.run')


class Employee(db.Model):
    """ Employees table. """

    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    birthday = db.Column(db.Date)
    salary = db.Column(db.Float, nullable=False)
    department_id = db.Column(db.Integer,
                              db.ForeignKey('departments.id'),
                              nullable=False)
    department = db.relationship('Department', backref='employees',
                                 primaryjoin=department_id == Department.id)
    working_since = db.Column(db.Date)

    def __init__(self, name: str, birthday: date, salary: float,
                 department_id: int, working_since: date = None):
        self.name = name
        self.birthday = birthday
        self.department_id = department_id
        self.working_since = working_since
        self.salary = salary
        logger.debug('Created Employee instance. Employee name is %s, '
                     'birthday = %s, department = %i, salary = %f, '
                     'working since %s',
                     self.name,
                     self.birthday,
                     self.department_id,
                     self.salary,
                     self.working_since)

    # def __eq__(self, other):
    #     if not isinstance(other, Employee):
    #         return NotImplemented
    #     return self.id == other.id \
    #            and self.name == other.name \
    #            and self.birthday == other.birthday \
    #            and self.department_id == other.department_id \
    #            and self.working_since == other.working_since \
    #            and self.salary == other.salary

    def __repr__(self):
        return f'<Employee {self.name} {self.birthday} {self.salary} >'
