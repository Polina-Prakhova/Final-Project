""" Description of Department table """
from . import db


class Department(db.Model):
    """ Description of 'departments' table. """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    avg_salary = db.Column(db.Float, nullable=False, server_default='0.0')
    count_employees = db.Column(db.Integer, nullable=False, server_default='0')
    email = db.Column(db.String(64))

    def __init__(self, name: str, email: str = ''):
        self.name = name
        self.email = email

    def __eq__(self, other):
        if not isinstance(other, Department):
            return NotImplemented
        return self.id == other.id \
               and self.name == other.name \
               and self.avg_salary == other.avg_salary \
               and self.count_employees == other.count_employees \
               and self.email == other.email

    def __repr__(self):
        return '<Department %r>' % self.name
