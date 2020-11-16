from flask import Flask
from views.index import departments_page

import config
from models.models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}/{config.DATABASE_NAME}'
db.init_app(app)

with app.app_context():
    db.create_all()


app.register_blueprint(departments_page)

if __name__ == "__main__":
    app.run(debug=True)
