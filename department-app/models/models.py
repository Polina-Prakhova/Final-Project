from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name: str):
        self.name = name

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

    def __init__(self, name: str, birthday: datetime, salary: float, department_id: int):
        self.name = name
        self.birthday = birthday
        self.salary = salary
        self.department_id = department_id

    def __repr__(self):
        return f'<Employee {self.name} {self.birthday} {self.salary} >'


class DepartmentInfo(db.Model):
    __tablename__ = 'department_info'

    id = db.Column(db.Integer, db.ForeignKey('departments.id'), primary_key=True)
    department = db.relationship('Department', backref='department_info', primaryjoin=id == Department.id)
    avg_salary = db.Column(db.Float, nullable=False)
    count_employees = db.Column(db.Integer, nullable=False)

    def __init__(self, department_id: int, avg_salary: float, count_employees: int):
        self.department_id = department_id
        self.avg_salary = avg_salary
        self.count_employees = count_employees

    def __repr__(self):
        return f'<Department №{self.id} {self.avg_salary} {self.count_employees}>'
