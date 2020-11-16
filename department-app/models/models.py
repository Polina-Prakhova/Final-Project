from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
 #   employees = db.relationship('Employee', backref='departments', lazy=True)
  #  number_of_employees = Column(Integer, nullable=False)
  #  average_salary = Column(Float, nullable=False)

    def __repr__(self):
        return '<Department %r>' % self.name


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    birthday = db.Column(db.DateTime)
    salary = db.Column(db.Float, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    department = db.relationship('Department', backref='employees', primaryjoin=department_id == Department.id)

    def __repr__(self):
        return f'<Employee {self.name} {self.birthday} {self.salary} >'