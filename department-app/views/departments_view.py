from flask import render_template

from service import department_service as ds
from . import departments_page


@departments_page.route('/', methods=['GET'])
@departments_page.route('/index', methods=['GET'])
@departments_page.route('/departments', methods=['GET'])
def show_all_departments():
    titles = ['№', 'Name', 'Average Salary', 'Employees']
    return render_template('departments.html',
                           title='Departments',
                           table_title='List of Departments',
                           headers=titles,
                           departments=ds.get_all())
