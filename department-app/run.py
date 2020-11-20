from flask import Flask
from flask_migrate import Migrate

from views import departments_view, employees_view, employee_view, department_view
from models import db


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')

    db.init_app(app)

 #   with app.app_context():
 #       db.create_all()

    app.register_blueprint(departments_view.departments_page)
    app.register_blueprint(employees_view.employees_page)
    app.register_blueprint(employee_view.employee_page)
    app.register_blueprint(department_view.department_page)

    migrate = Migrate(app, db)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
