""" Employees view """
from flask import render_template, request

from . import employees_page
from service import employee_service as es


@employees_page.route('/employees')
def show_all_employees():
    """ Render template with the list of all employees. """

    titles = ['№', 'Name', 'Birthday', 'In Department']
    employees = es.get_all()
    return render_template('employees.html',
                           title='Employees',
                           table_title='List of Employees',
                           headers=titles,
                           employees=employees)


@employees_page.route('/employees/')
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
