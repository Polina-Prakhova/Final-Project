from flask import render_template
from models.models import Department, Employee

from . import employee_page


@employee_page.route('/employees')
def show():
    lines = [{'name': 'dfasfasf', 'employees': 22, 'salary': 1},
             {'name': 'dfasfasf', 'employees': 22, 'salary': 1},
             {'name': 'dfasfasf', 'employees': 22, 'salary': 1},
             {'name': 'dfasfasf', 'employees': 22, 'salary': 1}]
    return render_template('employees.html', title='Employees',
                           headers=Department.query.all(), employees=Employee.query.all())
