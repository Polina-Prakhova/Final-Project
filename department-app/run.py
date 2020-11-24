""" Run file"""
from flask import Flask
from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_restful import Api

from views import departments_view, employees_view, employee_view, \
    department_view
from models import db
from rest.departments_api import DepartmentsAPI, DepartmentAPI
from rest.employees_api import EmployeeAPI, EmployeesAPI


def create_app():
    """ Setup before running. """
    application = Flask(__name__)

    application.config.from_pyfile('config.py')

    db.init_app(application)

    #   with application.app_context():
    #       db.create_all()

    # migrate = Migrate(application, db)

    manager = Manager(application)
    manager.add_command('db', MigrateCommand)

    application.register_blueprint(departments_view.departments_page)
    application.register_blueprint(employees_view.employees_page)
    application.register_blueprint(employee_view.employee_page)
    application.register_blueprint(department_view.department_page)

    api = Api(application)
    api.add_resource(DepartmentsAPI, '/api/departments', endpoint='departments')
    api.add_resource(DepartmentAPI, '/api/department/<int:id_>', endpoint='id')
    api.add_resource(EmployeesAPI, '/api/employees', endpoint='employees')
    api.add_resource(EmployeeAPI, '/api/employee/<int:id_>', endpoint='id_e')

    return application


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
