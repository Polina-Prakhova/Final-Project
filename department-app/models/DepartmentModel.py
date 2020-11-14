from app import db


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    number_of_employees = db.Column(db.Integer, nullable=False)
    average_salary = db.Column(db.FLOAT, nullable=False)

    def __repr__(self):
        return '<Department %r>' % self.name
