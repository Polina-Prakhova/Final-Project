from sqlalchemy import func

from models.department_model import Department
from models.employee_model import Employee, db


def get_all():
    """ Get all employees. """
    q = db.session.query(Employee)
    employees = q.all()
    db.session.commit()
    return employees


def get(id_: int):
    """ Get employee by id. """
    q = db.session.query(Employee)
    employee = q.filter(
        Employee.id == id_
    ).scalar()
    db.session.commit()
    return employee


def add(employee: Employee):
    """ Insert new employee. """
    db.session.add(employee)
    update_salary_and_employees(employee.department_id)
    db.session.commit()


def update(employee: Employee):
    """ Update existing employee. """
    update_employee = Employee.query.get(employee.id)
    update_employee = employee
    db.session.commit()


def delete(id_: int):
    """ Delete employee by id. """
    delete_employee = Employee.query.get(id_)
    db.session.delete(delete_employee)
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
    update_department.avg_salary = avg_salary
    update_department.count_employees = count_employees
    db.session.commit()
