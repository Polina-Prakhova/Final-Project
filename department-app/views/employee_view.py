""" Employee view """
from flask import render_template, url_for, request
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from service import employee_service as es
from service import department_service as ds

from . import employee_page


@employee_page.route('/employees/<int:id_>', methods=['GET'])
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


@employee_page.route("/employees/<int:id_>/delete", methods=["POST"])
def delete_employee(id_: int):
    """ Delete an employee. """
    employee = es.get(id_)

    if not employee:
        abort(404)

    es.delete(id_)

    return redirect(url_for("employees.show_all_employees"))


@employee_page.route("/employees/<int:id_>/update", methods=["GET", "POST"])
def update_employee(id_: int):
    """ Render page for editing an existing employee. """
    employee = es.get(id_)
    titles = ['№', 'Name', 'Birthday', 'In Department', 'Working Since',
              'Salary']
    return render_template('edit_employee.html',
                           title='Update employee',
                           table_title=f'Updating employee: {employee.name}',
                           headers=titles,
                           employee=employee,
                           departments=ds.get_all())


@employee_page.route("/employees/<int:id_>/update_done", methods=["POST"])
def update_done_employee(id_: int):
    """ Update an existing employee. """
    name = request.form.get("name")
    birthday = request.form.get("birthday")
    department = request.form.get("department_name")
    working_since = request.form.get("working_since")
    salary = request.form.get("salary")
    es.update(id_=id_, name=name, birthday=birthday, department=department,
              working_since=working_since, salary=salary)
    return redirect(url_for("employee.show_employee", id_=id_))


@employee_page.route("/employees/add", methods=["GET"])
def add_employee():
    """ Render page for adding a new employee. """
    titles = ['Name', 'Birthday', 'In Department', 'Working Since', 'Salary']
    return render_template('add_employee.html',
                           title='Add employee',
                           table_title='Adding new employee',
                           headers=titles,
                           departments=ds.get_all())


@employee_page.route("/employees/add_done", methods=["POST"])
def add_done_employee():
    """ Adding a new employee. """
    name = request.form.get("name")
    birthday = request.form.get("birthday")
    department = request.form.get("department")
    working_since = request.form.get("working_since")
    if not working_since:
        working_since = None
    salary = request.form.get("salary")
    es.add(name=name, birthday=birthday, department=department,
           working_since=working_since, salary=salary)
    return redirect(url_for("employees.show_all_employees"))
