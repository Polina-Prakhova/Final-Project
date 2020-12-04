""" File with functions for CRUD operation on Employees table."""
import logging
from datetime import date

from mysql.connector import IntegrityError

from models.employee_model import Employee, db

logger = logging.getLogger('department_app.run')


def get_all():
    """ Get all employees. """
    logger.debug('Retrieving all employees.')
    try:
        query = db.session.query(Employee)
        employees = query.all()
    except Exception as exception:
        logger.error('An error occurred while retrieving all employees'
                     ' Exception: %s', str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully retrieved all employees.')
    return employees


def get(id_: int):
    """ Get employee by id. """
    logger.debug('Retrieving employee by id %i.', id_)
    try:
        query = db.session.query(Employee)
        employee = query.filter(
            Employee.id == id_
        ).scalar()
        if not employee:
            raise IntegrityError(f"Can't get employee with id {id_}")
    except IntegrityError as exception:
        logger.error('An error occurred while retrieving employee with id %i.'
                     ' Exception: %s', id_, str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully retrieved employee by id %i.', id_)
    return employee


def get_by_name(name: str):
    """ Get employee by name. """
    logger.debug('Retrieving employee by name %s.', name)
    try:
        query = db.session.query(Employee)
        employee = query.filter(
            Employee.name == name
        ).scalar()
    except Exception as exception:
        logger.error('An error occurred while retrieving employee by name %s.'
                     ' Exception: %s', name, str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully retrieved employee by name %s.', name)
    return employee


def add(name: str, birthday: date, department: int, working_since: date,
        salary: float):
    """ Insert new employee. """
    logger.debug('Adding employee with name %s.', name)
    new_employee = Employee(name, birthday, salary, department, working_since)
    try:
        db.session.add(new_employee)
    except Exception as exception:
        logger.error('An error occurred while adding employee with name %s. '
                     'Exception: %s', name, str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully added new employee with name %s.', name)
    return new_employee.id


def update(id_: int, name: str, birthday: date, department: int,
           working_since: date, salary: float):
    """ Update existing employee. """
    logger.debug('Updating employee with id %i, name %s, birthday %s, '
                 'department %i, salary %f and working since %s.',
                 id_, name, birthday, department, salary, working_since)

    try:
        query = db.session.query(Employee)
        employee = query.filter(
            Employee.id == id_
        ).scalar()
        employee.name = name
        employee.birthday = birthday
        employee.department_id = department
        employee.working_since = working_since
        employee.salary = salary
    except Exception as exception:
        logger.error('An error occurred while updating employee with id %i. '
                     'Exception: %s', id_, str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully updated employee with id %i.', id_)


def delete(id_: int):
    """ Delete employee by id. """
    logger.debug('Deleting employee with id %i.', id_)
    try:
        delete_employee = Employee.query.get(id_)
        db.session.delete(delete_employee)
    except Exception as exception:
        logger.error('An error occurred while deleting employee with id %i. '
                     'Exception: %s', id_, str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully deleted employee with id %i.', id_)


def delete_all():
    """ Delete all employees. """
    logger.debug('Deleting all employees.')
    try:
        for employee in get_all():
            delete_employee = Employee.query.get(employee.id)
            db.session.delete(delete_employee)
    except Exception as exception:
        logger.error('An error occurred while deleting employees. '
                     'Exception: %s', str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully deleted all employees.')


def find_by_birthday(start: date, end: date):
    """ Find employees by birthday between start and end. """
    logger.debug('Retrieving all employees with birthday between %s and %s.',
                 start, end)
    try:
        employees = db.session.query(
            Employee
        ).filter(
            Employee.birthday >= start
        ).filter(
            Employee.birthday <= end
        ).all()
    except Exception as exception:
        logger.error('An error occurred while retrieving employees. '
                     'Exception: %s', str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully retrieved all employees with birthday '
                'between %s and %s (amount = %i).', start, end, len(employees))
    return employees
