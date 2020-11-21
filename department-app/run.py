from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from views import departments_view, employees_view, employee_view, \
    department_view
from models import *


def create_app():
    application = Flask(__name__)

    application.config.from_pyfile('config.py')

    db.init_app(application)

    #   with application.app_context():
    #       db.create_all()

    migrate = Migrate(application, db)

    manager = Manager(application)
    manager.add_command('db', MigrateCommand)

    application.register_blueprint(departments_view.departments_page)
    application.register_blueprint(employees_view.employees_page)
    application.register_blueprint(employee_view.employee_page)
    application.register_blueprint(department_view.department_page)

    return application


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
