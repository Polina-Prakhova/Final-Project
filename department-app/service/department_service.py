from sqlalchemy import func

from models.department_model import Department, db
from models.employee_model import Employee


def get_all():
    """ Get all departments. """
    try:
        q = db.session.query(Department)
        departments = q.all()
        for dep in departments:
            update_salary_and_employees(dep.id)
    except Exception:
        db.session.rollback()
        raise
    db.session.commit()
    return departments


def get(id_: int):
    """ Get department by id. """
    try:
        q = db.session.query(Department)
        department = q.filter(
            Department.id == id_
        ).scalar()
    except Exception:
        db.session.rollback()
        raise
    db.session.commit()
    return department


def add(name: str, email: str = None):
    """ Insert new department. """
    new_department = Department(name, email)
    try:
        db.session.add(new_department)
    except Exception:
        db.session.rollback()
        raise
    db.session.commit()
    return new_department.id


def update(id_: int, name: str, email: str):
    """ Update existing department. """
    try:
        q = db.session.query(Department)
        department = q.filter(
            Department.id == id_
        ).scalar()
        department.name = name
        department.email = email
    except Exception:
        db.session.rollback()
        raise
    db.session.commit()


def delete(id_: int):
    """ Delete department by id. """
    try:
        q = db.session.query(Department)
        delete_department = q.filter(
            Department.id == id_
        ).scalar()
        db.session.delete(delete_department)
    except Exception:
        db.session.rollback()
        raise
    db.session.commit()


def update_salary_and_employees(id_: int):
    """ Recalculate fields avg_salary and count_employees in Department
    after adding new employee."""
    try:
        avg_salary = db.session.query(
            func.avg(Employee.salary)
        ).filter(
            Employee.department_id == Department.id
        ).filter(
            Department.id == id_
        ).scalar()

        count_employees = db.session.query(
            func.count(Employee.id)
        ).filter(
            Employee.department_id == Department.id
        ).filter(
            Department.id == id_
        ).scalar()

        update_department = Department.query.get(id_)
        update_department.avg_salary = 0.0 if not avg_salary else avg_salary
        update_department.count_employees = \
            0 if not count_employees else count_employees
    except Exception:
        db.session.rollback()
        raise
    db.session.commit()
