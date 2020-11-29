""" Run file"""
import logging

from sqlalchemy_utils import create_database, database_exists
from flask import Flask
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager
from flask_restful import Api

from views import employee_view, department_view
from models import db
from rest.departments_api import DepartmentsAPI, DepartmentAPI
from rest.employees_api import EmployeeAPI, EmployeesAPI

logger = logging.getLogger('department_app.run')


def logging_configuration():
    """ Configuration for logging - setting levels, log file, format etc."""
    log = logging.getLogger('department_app')
    log.setLevel(logging.DEBUG)

    log_file = logging.FileHandler('department_app.log')
    log_file.setLevel(logging.DEBUG)

    stream = logging.StreamHandler()
    stream.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s : %(message)s')
    log_file.setFormatter(formatter)
    stream.setFormatter(formatter)

    log.addHandler(log_file)
    log.addHandler(stream)


def create_app():
    """ Setup before running. """
    logging_configuration()

    application = Flask(__name__)
    logger.debug('Created Flask instance.')

    application.config.from_pyfile('config.py')
    logger.debug('Set configuration parameters for the application. DB '
                 'host:port = %s:%s', application.config.get("DATABASE_HOST"),
                 application.config.get("DATABASE_PORT"))

    db.init_app(application)
    logger.debug('Initialized application for database.')

    migrate = Migrate(application, db)
    manager = Manager(application)
    manager.add_command('db', MigrateCommand)

    if not database_exists(application.config['SQLALCHEMY_DATABASE_URI']):
        create_database(application.config['SQLALCHEMY_DATABASE_URI'])
        logger.debug('Created database.')

    with application.app_context():
        db.create_all()
        logger.debug('Created all tables.')

    application.register_blueprint(employee_view.employee_page)
    application.register_blueprint(department_view.department_page)
    logger.debug('Registered blueprint for all views.')

    api = Api(application)
    api.add_resource(DepartmentsAPI, '/api/departments', endpoint='departments')
    api.add_resource(DepartmentAPI, '/api/departments/<int:id_>', endpoint='id')
    api.add_resource(EmployeesAPI, '/api/employees', endpoint='employees')
    api.add_resource(EmployeeAPI, '/api/employees/<int:id_>', endpoint='id_e')
    logger.debug('Added resources for all views.')

    return application


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
