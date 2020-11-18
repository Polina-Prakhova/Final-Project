from flask import render_template

from models.models import Department
from service import department_service as ds, department_info_service as dis
from . import departments_page


@departments_page.route('/')
@departments_page.route('/index')
@departments_page.route('/departments')
def show():
    return render_template('departments.html', title='Departments',
                           headers=Department.query.all(), departments=ds.get_all())
