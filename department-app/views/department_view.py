""" Department view """
from flask import render_template, url_for, request
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from service import department_service as ds
from . import department_page


@department_page.route('/departments/<int:id_>', methods=['GET'])
def show_department(id_: int):
    """ Render template with the information of certain department. """
    titles = ['№', 'Name', 'Average Salary', 'Employees', 'E-mail']
    department = ds.get(id_)
    return render_template('department.html',
                           title='Department',
                           table_title=f'Department: {department.name}',
                           headers=titles,
                           department=department)


@department_page.route("/departments/<int:id_>/delete", methods=["POST"])
def delete_department(id_: int):
    """Delete an department."""
    department = ds.get(id_)

    if not department:
        abort(404)

    ds.delete(id_)

    return redirect(url_for("departments.show_all_departments"))


@department_page.route("/departments/<int:id_>/update", methods=["GET", "POST"])
def update_department(id_: int):
    """ Render page for editing an existing department. """
    department = ds.get(id_)
    titles = ['№', 'Name', 'Average Salary', 'Employees', 'E-mail']
    return render_template('edit_department.html',
                           title='Update department',
                           table_title=f'Updating department: '
                                       f'{department.name}',
                           headers=titles,
                           department=department)


@department_page.route("/departments/<int:id_>/update_done", methods=["POST"])
def update_done_department(id_: int):
    """ Update an existing department. """
    name = request.form.get("name")
    email = request.form.get("email")
    ds.update(id_, name, email)
    return redirect(url_for("department.show_department", id_=id_))
