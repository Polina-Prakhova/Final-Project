from datetime import date

from sqlalchemy.exc import IntegrityError

from models.employee_model import Employee, db


def get_all():
    """ Get all employees. """
    try:
        q = db.session.query(Employee)
        employees = q.all()
    except Exception:
        db.session.rollback()
        raise
    db.session.commit()
    return employees


def get(id_: int):
    """ Get employee by id. """
    try:
        q = db.session.query(Employee)
        employee = q.filter(
            Employee.id == id_
        ).scalar()
    except Exception:
        db.session.rollback()
        raise
    db.session.commit()
    return employee


def add(employee: Employee):
    """ Insert new employee. """
    try:
        db.session.add(employee)
    except Exception:
        db.session.rollback()
        raise
    db.session.commit()


def update(id_: int, name: str, birthday: date, department: int,
           working_since: date, salary: float):
    """ Update existing employee. """
    try:
        q = db.session.query(Employee)
        employee = q.filter(
            Employee.id == id_
        ).scalar()
        employee.name = name
        employee.birthday = birthday
        employee.department_id = department
        employee.working_since = working_since
        employee.salary = salary
    except Exception:
        db.session.rollback()
        raise
    db.session.commit()


def delete(id_: int):
    """ Delete employee by id. """
    try:
        delete_employee = Employee.query.get(id_)
        db.session.delete(delete_employee)
    except Exception:
        db.session.rollback()
        raise
    db.session.commit()


def find_by_birthday(start: date, end: date):
    """ Find employees by birthday between start and end. """
    try:
        employees = db.session.query(
            Employee
        ).filter(
            Employee.birthday >= start
        ).filter(
            Employee.birthday <= end
        ).all()
    except Exception:
        db.session.rollback()
        raise
    db.session.commit()
    return employees
