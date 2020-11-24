""" Creating Blueprints for views. """
from flask import Blueprint


TEMPLATE_FOLDER = 'templates'

departments_page = Blueprint(
    'departments', __name__, template_folder=TEMPLATE_FOLDER)
employees_page = Blueprint(
    'employees', __name__, template_folder=TEMPLATE_FOLDER)
employee_page = Blueprint(
    'employee', __name__, template_folder=TEMPLATE_FOLDER)
department_page = Blueprint(
    'department', __name__, template_folder=TEMPLATE_FOLDER)
