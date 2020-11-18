from flask import render_template

from . import departments_page


@departments_page.route('/')
@departments_page.route('/index')
@departments_page.route('/departments')
def show():
    return render_template('departments.html', title='Departments')
