from datetime import datetime

from models.models import Employee, db


def get_all():
    return Employee.query.all()


def add(name: str, birthday: datetime, salary: float, department_id: int):
    new_employee = Employee(name, birthday, salary, department_id)
    db.session.add(new_employee)
    db.session.commit()
