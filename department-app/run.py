from flask import Flask
from flask_migrate import Migrate

from views import departments, employees
from models.models import db


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')

    db.init_app(app)
 #   with app.app_context():
 #       db.create_all()

    app.register_blueprint(departments.departments_page)
    app.register_blueprint(employees.employees_page)

    migrate = Migrate(app, db)

    return app


if __name__ == "__main__":
    app = create_app()
    print(app.url_map)
    app.run(debug=True)
