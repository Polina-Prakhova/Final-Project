""" Departments view """
import os
import sys

from flask import render_template

current_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(current_path, '..')
sys.path.append(ROOT_PATH)

# pylint: disable=wrong-import-position
from service import department_service as ds
from views import departments_page
# pylint: enable=wrong-import-position


@departments_page.route('/', methods=['GET'])
@departments_page.route('/departments', methods=['GET'])
def show_all_departments():
    """ Render template with the list of all departments. """
    titles = ['№', 'Name', 'Average Salary', 'Employees']
    departments = ds.get_all()
    return render_template('departments.html',
                           title='Departments',
                           table_title='List of Departments',
                           headers=titles,
                           departments=departments)
