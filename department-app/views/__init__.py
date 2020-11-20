from flask import Blueprint


template_folder = 'templates'

departments_page = Blueprint(
    'departments', __name__, template_folder=template_folder)
employees_page = Blueprint(
    'employees', __name__, template_folder=template_folder)
employee_page = Blueprint(
    'employee', __name__, template_folder=template_folder)
department_page = Blueprint(
    'department', __name__, template_folder=template_folder)
