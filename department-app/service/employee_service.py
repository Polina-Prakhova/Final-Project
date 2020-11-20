from datetime import date

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
    db.session.commit()


def update(employee: Employee):
    """ Update existing employee. """
    Employee.query.get(employee.id).update(
        {Employee.name: employee.name,
         Employee.birthday: employee.birthday,
         Employee.salary: employee.salary,
         Employee.department_id: employee.department_id,
         Employee.working_since: employee.working_since})
    db.session.commit()


def delete(id_: int):
    """ Delete employee by id. """
    delete_employee = Employee.query.get(id_)
    db.session.delete(delete_employee)
    db.session.commit()


def find_by_birthday(start: date, end: date):
    """ Find employees by birthday between start and end. """
    employees = db.session.query(
        Employee
    ).filter(
        Employee.birthday >= start
    ).filter(
        Employee.birthday <= end
    ).all()
    return employees
