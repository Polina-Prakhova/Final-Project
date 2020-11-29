""" Department view """
import logging
import os
import sys

import sqlalchemy.exc
from flask import render_template, url_for, request
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

current_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(current_path, '..')
sys.path.append(ROOT_PATH)

# pylint: disable=wrong-import-position
from service import department_service as ds
from views import department_page

# pylint: enable=wrong-import-position

logger = logging.getLogger('department_app.run')


@department_page.route('/', methods=['GET'])
@department_page.route('/departments', methods=['GET'])
def show_all_departments():
    """ Render template with the list of all departments. """

    logger.debug('Function show_all_departments(). Routed to /departments')
    titles = ['№', 'Name', 'Average Salary', 'Employees']
    departments = ds.get_all()
    logger.info('Get list of departments, length is %i', len(departments))
    return render_template('departments.html',
                           title='Departments',
                           table_title='List of Departments',
                           headers=titles,
                           departments=departments)


@department_page.route('/departments/<int:id_>', methods=['GET'])
def show_department(id_: int):
    """ Render template with the information of certain department. """

    logger.debug('Routed to /departments/%i', id_)
    titles = ['№', 'Name', 'Average Salary', 'Employees', 'E-mail']
    department = ds.get(id_)
    if not department:
        logger.error("Can't find department with id %i", id_)
        abort(404)

    logger.info('Get department %s', department.name)
    return render_template('department.html',
                           title='Department',
                           table_title=f'Department: {department.name}',
                           headers=titles,
                           department=department)


@department_page.route("/departments/<int:id_>/delete", methods=["POST"])
def delete_department(id_: int):
    """Delete an department."""
    logger.debug('Routed to /departments/%i/delete', id_)
    department = ds.get(id_)

    if not department:
        logger.error("Can't deleted department %s", department.name)
        abort(404)

    ds.delete(id_)
    logger.info('Successfully deleted department %s', department.name)

    return redirect(url_for("departments.show_all_departments"))


@department_page.route("/departments/<int:id_>/update", methods=["GET", "POST"])
def update_department(id_: int):
    """ Render page for editing an existing department. """
    logger.debug('Routed to /departments/%i/update', id_)
    department = ds.get(id_)

    if not department:
        logger.error("Can't get department with id %i", id_)
        abort(404)

    titles = ['№', 'Name', 'Average Salary', 'Employees', 'E-mail']
    logger.info('Get department %s', department.name)
    return render_template('edit_department.html',
                           title='Update department',
                           table_title=f'Updating department: '
                                       f'{department.name}',
                           headers=titles,
                           department=department)


@department_page.route("/departments/<int:id_>/update_done", methods=["POST"])
def update_done_department(id_: int):
    """ Update an existing department. """
    logger.debug('Routed to /departments/%i/update_done', id_)
    name = request.form.get("name")
    email = request.form.get("email")
    try:
        ds.update(id_, name, email)
    except sqlalchemy.exc.IntegrityError as exception:
        logger.error('Can\'t update department with name %s and email %s. '
                     'Exception: %s', name, email, exception.orig)
        abort(404)
    logger.info('Successfully updated department with id %i. It\'s name = %s, '
                'email = %s', id_, name, email)
    return redirect(url_for("department.show_department", id_=id_))


@department_page.route("/departments/add", methods=["GET"])
def add_department():
    """ Render page for adding a new department. """
    logger.debug('Routed to /departments/add')
    titles = ['Name', 'E-mail']
    return render_template('add_department.html',
                           title='Add department',
                           table_title='Adding new department',
                           headers=titles)


@department_page.route("/departments/adding", methods=["POST"])
def add_done_department():
    """ Update an existing department. """
    logger.debug('Routed to /departments/add_done')
    name = request.form.get("name")
    email = request.form.get("email")

    try:
        ds.add(name, email)
    except sqlalchemy.exc.IntegrityError as exception:
        logger.error('Can\'t add department with name %s and email %s. '
                     'Exception: %s', name, email, exception.orig)
        abort(404)
    return redirect(url_for("department.show_all_departments"))
