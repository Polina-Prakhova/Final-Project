from flask import render_template, Blueprint
from ..models.models import Department, Employee

departments_page = Blueprint('departments_page', __name__,
                             template_folder='templates')


@departments_page.route('/')
@departments_page.route('/index')
@departments_page.route('/departments')
def show():
    lines = [{'name': 'dfasfasf', 'employees': 22, 'salary': 1},
             {'name': 'dfasfasf', 'employees': 22, 'salary': 1},
             {'name': 'dfasfasf', 'employees': 22, 'salary': 1},
             {'name': 'dfasfasf', 'employees': 22, 'salary': 1}]
    return render_template('departments.html', title='Departments',
                           headers=Department.query.all(), departments=Employee.query.all())
