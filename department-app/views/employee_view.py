""" Employee view """
import logging
import os
import sys
from datetime import date

from sqlalchemy.exc import IntegrityError
from flask import render_template, url_for, request
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

current_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(current_path, '..')
sys.path.append(ROOT_PATH)

# pylint: disable=wrong-import-position
from service import employee_service as es
from service import department_service as ds
from views import employee_page

# pylint: enable=wrong-import-position

logger = logging.getLogger('department_app.run')


@employee_page.route('/employees', methods=['GET'])
def show_all_employees():
    """ Render template with the list of all employees. """

    logger.debug('Function show_all_employees(). Routed to /employees')
    titles = ['Name', 'Birthday', 'In Department']
    employees = es.get_all()

    logger.info('Get list of employees, length = %i', len(employees))
    return render_template('employees.html',
                           title='Employees',
                           table_title='List of Employees',
                           headers=titles,
                           date=date.today(),
                           employees=employees)


@employee_page.route('/employees/search', methods=['GET'])
def show_employees_birthday():
    """ Render template with the list of employees
    whose birthdays are in specific period. """

    logger.debug('Function show_employees_birthday(). Routed to /employees')
    titles = []
    message = 'No results'

    start = request.args.get('start')
    end = request.args.get('end')
    employees = es.find_by_birthday(start, end)
    logger.debug('Get employees with birthday between %s and %s. Amount = %i',
                 start, end, len(employees))

    if employees:
        titles = ['Name', 'Birthday', 'In Department']
        message = f'Find {len(employees)} employee(s)'

    return render_template('employees.html',
                           title='Employees',
                           table_title='List of Employees',
                           headers=titles,
                           message=message,
                           employees=employees)


@employee_page.route('/employees/<int:id_>', methods=['GET'])
def show_employee(id_: int):
    """ Render template with the information of certain employee. """

    logger.debug('Routed to /employees/%i', id_)
    titles = ['Name', 'Birthday', 'In Department', 'Working Since',
              'Salary']
    employee = None

    try:
        employee = es.get(id_)
    except IntegrityError:
        logger.error("Can't find employee with id %i", id_)
        abort(404)

    logger.info('Got employee %s', employee.name)
    return render_template('employee.html',
                           title=f'Employee {employee.name}',
                           table_title=f'Employee: {employee.name}',
                           headers=titles,
                           employee=employee)


@employee_page.route("/employees/<int:id_>/delete", methods=["POST"])
def delete_employee(id_: int):
    """ Delete an employee. """

    logger.debug('Routed to /employees/%i/delete', id_)
    employee = None

    try:
        employee = es.get(id_)
    except IntegrityError:
        logger.error("Can't deleted employee with id %i", id_)
        abort(404)

    es.delete(id_)
    logger.info('Successfully deleted employee %s', employee.name)

    return redirect(url_for("employee.show_all_employees"))


@employee_page.route("/employees/<int:id_>/update", methods=["GET", "POST"])
def update_employee(id_: int):
    """ Render page for editing an existing employee. """
    logger.debug('Routed to /employees/%i/update', id_)

    if request.method == 'POST':
        name = request.form.get("name")
        birthday = request.form.get("birthday")
        department = int(request.form.get("department_name"))
        working_since = request.form.get("working_since")
        salary = float(request.form.get("salary"))
        try:
            es.update(id_=id_, name=name, birthday=birthday,
                      department=department,
                      working_since=working_since, salary=salary)
        except IntegrityError as exception:
            logger.error('Can\'t update employee with name %s, birthday %s, '
                         'department %i, salary %f and working since %s. '
                         'Exception: %s', name, birthday, department, salary,
                         working_since, str(exception))
            abort(404)
        except Exception:
            abort(404)

        logger.info('Successfully updated employee with id {}. It\'s name %s, '
                    'birthday %s, department %i, salary %f and '
                    'working since %s. ',
                    name, birthday, department, salary, working_since)
        return redirect(url_for("employee.show_employee", id_=id_))

    employee = None
    try:
        employee = es.get(id_)
    except IntegrityError:
        logger.error("Can't update employee with id %i", id_)
        abort(404)

    titles = ['Name', 'Birthday', 'In Department', 'Working Since',
              'Salary']
    logger.info('Get employee %s', employee.name)
    return render_template('edit_employee.html',
                           title='Update employee',
                           table_title=f'Updating employee: {employee.name}',
                           headers=titles,
                           employee=employee,
                           departments=ds.get_all())


@employee_page.route("/employees/add", methods=["GET", "POST"])
def add_employee():
    """ Adding a new employee. """
    logger.debug('Routed to /employees/add')

    if request.method == 'POST':
        name = request.form.get("name")
        birthday = request.form.get("birthday")
        department = int(request.form.get("department"))
        working_since = request.form.get("working_since")
        if not working_since:
            working_since = None
        salary = float(request.form.get("salary"))
        try:
            es.add(name=name, birthday=birthday, department=department,
                   working_since=working_since, salary=salary)
        except IntegrityError as exception:
            logger.error('Can\'t add employee with name %s, birthday %s, '
                         'department %i, salary %f and working since %s. '
                         'Exception: %s', name, birthday, department, salary,
                         working_since, str(exception))
            abort(404)

        logger.debug(
            'Successfully added new employee with name %s, birthday %s, '
            'department %i, salary %f and working since %s.',
            name, birthday, department, salary, working_since)
        return redirect(url_for("employee.show_all_employees"))

    titles = ['Name', 'Birthday', 'In Department', 'Working Since', 'Salary']
    return render_template('add_employee.html',
                           title='Add employee',
                           table_title='Adding new employee',
                           headers=titles,
                           departments=ds.get_all())
