""" Description of Employee table """
from datetime import date

from models.department_model import Department
from . import db


class Employee(db.Model):
    """ Description of 'employees' table. """

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

    def __repr__(self):
        return f'<Employee {self.name} {self.birthday} {self.salary} >'
