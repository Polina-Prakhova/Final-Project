from flask import render_template

from service import department_service as ds
from . import department_page


@department_page.route('/departments/<int:id_>', methods=['GET'])
def show_department(id_):
    titles = ['№', 'Name', 'Average Salary', 'Employees']
    department = ds.get(id_)
    return render_template('department.html',
                           title='Department',
                           table_title=f'Department: {department.name}',
                           headers=titles,
                           department=department)
