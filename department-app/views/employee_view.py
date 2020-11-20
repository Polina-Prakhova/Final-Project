""" Employee view """
from flask import render_template
from service import employee_service as es

from . import employee_page


@employee_page.route('/employees/<int:id_>')
def show_employee(id_: int):
    """ Render template with the information of certain employee. """

    titles = ['№', 'Name', 'Birthday', 'In Department', 'Working Since',
              'Salary']
    employee = es.get(id_)
    return render_template('employee.html',
                           title='Employee',
                           table_title=f'Employee: {employee.name}',
                           headers=titles,
                           employee=employee)
