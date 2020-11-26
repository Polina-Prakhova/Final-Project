""" Employees view """
import os
import sys
from datetime import date

from flask import render_template, request

current_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(current_path, '..')
sys.path.append(ROOT_PATH)

# pylint: disable=wrong-import-position
from service import employee_service as es
from views import employees_page
# pylint: enable=wrong-import-position


@employees_page.route('/employees', methods=['GET'])
def show_all_employees():
    """ Render template with the list of all employees. """

    titles = ['№', 'Name', 'Birthday', 'In Department']
    employees = es.get_all()
    return render_template('employees.html',
                           title='Employees',
                           table_title='List of Employees',
                           headers=titles,
                           date=date.today(),
                           employees=employees)


@employees_page.route('/employees/', methods=['GET'])
def show_employees_birthday():
    """ Render template with the list of employees
    whose birthdays are in specific period. """

    start_b = request.args.get('start_b')
    end_b = request.args.get('end_b')
    employees = es.find_by_birthday(start_b, end_b)
    titles = []
    message = 'No results'
    if employees:
        titles = ['№', 'Name', 'Birthday', 'In Department']
        message = f'Find {len(employees)} employee(s)'
    return render_template('employees.html',
                           title='Employees',
                           table_title='List of Employees',
                           headers=titles,
                           message=message,
                           employees=employees)
