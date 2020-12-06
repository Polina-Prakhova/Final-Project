""" Department view """
import logging
import os
import sys

from sqlalchemy.exc import IntegrityError
from flask import render_template, url_for, request, session, flash
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
    titles = ['Name', 'Average Salary', 'Employees']
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
    titles = ['Name', 'Average Salary', 'Employees', 'E-mail']
    department = None

    try:
        department = ds.get(id_)
    except IntegrityError:
        logger.error("Can't find employee with id %i", id_)
        abort(404)

    logger.info('Get department %s', department.name)
    return render_template('department.html',
                           title=f'Department {department.name}',
                           table_title=f'Department: {department.name}',
                           headers=titles,
                           department=department)


@department_page.route("/departments/<int:id_>/delete", methods=["POST"])
def delete_department(id_: int):
    """Delete an department."""
    logger.debug('Routed to /departments/%i/delete', id_)
    department = None

    try:
        department = ds.get(id_)
    except IntegrityError:
        logger.error("Can't delete department with id %i", id_)
        abort(404)

    ds.delete(id_)
    logger.info('Successfully deleted department %s', department.name)

    return redirect(url_for("department.show_all_departments"))


@department_page.route("/departments/<int:id_>/update", methods=["GET", "POST"])
def update_department(id_: int):
    """ Editing an existing department. """
    logger.debug('Routed to /departments/%i/update', id_)

    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")

        try:
            ds.update(id_, name, email)
        except IntegrityError as exception:
            logger.error('Can\'t update department with name %s and email %s. '
                         'Exception: %s', name, email, str(exception))

            session['name'] = name
            session['email'] = email
            flash(f'Department with name {name} already exists.')
            return redirect(request.referrer)

        except Exception as exception:
            logger.error('Can\'t add department with name %s and email %s. '
                         'Exception: %s', name, email, str(exception))
            abort(404)

        logger.info(
            'Successfully updated department with id %i. It\'s name = %s, '
            'email = %s', id_, name, email)
        return redirect(url_for("department.show_department", id_=id_))

    department = None
    try:
        department = ds.get(id_)
    except IntegrityError:
        logger.error("Can't get department with id %i", id_)
        abort(404)

    titles = ['Name', 'Average Salary', 'Employees', 'E-mail']
    logger.info('Get department %s', department.name)
    return render_template('edit_department.html',
                           title='Update department',
                           table_title=f'Updating department: '
                                       f'{department.name}',
                           headers=titles,
                           department=department)


@department_page.route("/departments/add", methods=["GET", "POST"])
def add_department():
    """ Adding a new department. """
    logger.debug('Routed to /departments/add')

    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")

        try:
            ds.add(name, email)
        except IntegrityError as exception:
            logger.error('Can\'t add department with name %s and email "%s". '
                         'Exception: %s', name, email, str(exception))
            session['name'] = name
            session['email'] = email
            flash(f'Department with name {name} already exists.')
            return redirect(request.referrer)
        except Exception as exception:
            logger.error('Can\'t add department with name %s and email %s. '
                         'Exception: %s', name, email, str(exception))
            abort(404)
        return redirect(url_for('department.show_all_departments'))

    titles = ['Name', 'E-mail']
    return render_template('add_department.html',
                           title='Add department',
                           table_title='Adding new department',
                           headers=titles)

