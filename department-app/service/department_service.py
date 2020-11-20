from sqlalchemy import func

from models.department_model import Department, db
from models.employee_model import Employee


def get_all():
    """ Get all departments. """
    q = db.session.query(Department)
    departments = q.all()
    for dep in departments:
        update_salary_and_employees(dep.id)
    db.session.commit()
    return departments


def get(id_: int):
    """ Get department by id. """
    q = db.session.query(Department)
    department = q.filter(
        Department.id == id_
    ).scalar()
    db.session.commit()
    return department


def add(department: Department):
    """ Insert new department. """
    new_department = department
    db.session.add(new_department)
    db.session.commit()


def update(department: Department):
    """ Update existing department. """
    Department.query.get(department.id).update(
        {Department.name: department.name})
    db.session.commit()


def delete(id_: int):
    """ Delete department by id. """
    delete_department = Department.query.get(id_)
    db.session.delete(delete_department)
    db.session.commit()


def update_salary_and_employees(id_: int):
    """ Recalculate fields avg_salary and count_employees in Department
    after adding new employee."""
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
    db.session.commit()
