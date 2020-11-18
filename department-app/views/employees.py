from flask import render_template
from models.models import Department, Employee

from . import employees_page


@employees_page.route('/employees')
def show():
    return render_template('employees.html', title='Employees',
                           headers=Department.query.all(), employees=Employee.query.all())
