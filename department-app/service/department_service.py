""" File with functions for CRUD operation on Departments table."""
import logging

from sqlalchemy import func

from models.department_model import Department, db
from models.employee_model import Employee

logger = logging.getLogger('department_app.run')


def get_all():
    """ Get all departments. """
    logger.debug('Retrieving all departments.')
    try:
        query = db.session.query(Department)
        departments = query.all()
        for dep in departments:
            __update_salary_and_employees(dep.id)
    except Exception as exception:
        logger.error('An error occurred while retrieving all departments'
                     ' Exception: %s', str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully retrieved all departments.')
    return departments


def get(id_: int):
    """ Get department by id. """
    logger.debug('Retrieving department by id %i.', id_)
    try:
        query = db.session.query(Department)
        department = query.filter(
            Department.id == id_
        ).scalar()

        if not department:
            raise Exception(f"Can't get department with id {id_}")

    except Exception as exception:
        logger.error('An error occurred while retrieving department with id %i.'
                     ' Exception: %s', id_, str(exception))
        db.session.rollback()
        raise

    db.session.commit()
    logger.info('Successfully retrieved department by id %i.', id_)
    return department


def get_by_name(name: str):
    """ Get department by name. """
    logger.debug('Retrieving department by name %s.', name)
    try:
        query = db.session.query(Department)
        department = query.filter(
            Department.name == name
        ).scalar()

        if not department:
            raise Exception(f"Can't get department with name {name}")

    except Exception as exception:
        logger.error('An error occurred while retrieving department by name %s.'
                     ' Exception: %s', name, str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully retrieved department by name %s.', name)
    return department


def add(name: str, email: str = ''):
    """ Insert new department. """
    logger.debug('Adding department with name %s and email %s.', name, email)
    new_department = Department(name, email)
    try:
        db.session.add(new_department)
    except Exception as exception:
        logger.error('An error occurred while adding department with name %s '
                     'and email %s. Exception: %s', name, email, str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully added new department with name %s and email %s.',
                name, email)
    return new_department.id


def update(id_: int, name: str, email: str = ''):
    """ Update existing department. """
    logger.debug('Updating department with id %i, name %s and email %s.',
                 id_, name, email)
    try:
        query = db.session.query(Department)
        if not query.filter(Department.id == id_).scalar():
            raise Exception(f"Can't update department with id {id_}")
        query.filter(Department.id == id_).\
            update(dict(name=name, email=email))
    except Exception as exception:
        logger.error('An error occurred while updating department with id %i. '
                     'Exception: %s', id_, str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully updated department with id %i.', id_)


def delete(id_: int):
    """ Delete department by id. """
    logger.debug('Deleting department with id %i.', id_)
    try:
        query = db.session.query(Department)
        delete_department = query.filter(
            Department.id == id_
        ).scalar()

        if not delete_department:
            raise Exception(f"Can't delete department with id {id_}")

        db.session.delete(delete_department)
    except Exception as exception:
        logger.error('An error occurred while deleting department with id %i. '
                     'Exception: %s', id_, str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully deleted department with id %i.', id_)


def delete_all():
    """ Delete all departments. """
    logger.debug('Deleting all departments.')
    try:
        for department in get_all():
            delete_department = Department.query.get(department.id)
            db.session.delete(delete_department)
    except Exception as exception:
        logger.error('An error occurred while deleting departments. '
                     'Exception: %s', str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully deleted all departments.')


def __update_salary_and_employees(id_: int):
    """ Recalculate fields avg_salary and count_employees in Department
    after adding new employee."""
    logger.debug('Updating average salary in department and employees '
                 'amount in it.')
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
    except Exception as exception:
        logger.error('An error occurred while updating average salary and '
                     'employees amount in department. Exception: %s',
                     str(exception))
        db.session.rollback()
        raise
    db.session.commit()
    logger.info('Successfully updated average salary and employees amount.')
