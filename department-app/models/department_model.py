from . import db


class Department(db.Model):
    """ Description of 'departments' table. """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    avg_salary = db.Column(db.Float, nullable=False, server_default='0.0')
    count_employees = db.Column(db.Integer, nullable=False, server_default='0')

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return '<Department %r>' % self.name
