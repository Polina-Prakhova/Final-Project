from models.models import Department, db


def get_all():
    return Department.query.all()


def add(name: str):
    new_department = Department(name)
    new = db.session.add(new_department)
    db.session.commit()
