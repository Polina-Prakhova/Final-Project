from models.department_model import Department, db


def get_all():
    """ Get all departments. """
    q = db.session.query(Department)
    departments = q.all()
    db.session.commit()
    return departments


def get(id_: int):
    """ Get department by id. """
    q = db.session.query(Department)
    department = q.filter(
        Department.id == id_
    ).scalar()
    db.session.commit()
    return department


def add(department: Department):
    """ Insert new department. """
    new_department = department
    new = db.session.add(new_department)
    db.session.commit()


def update(department: Department):
    """ Update existing department. """
    update_department = Department.query.get(department.id)
    update_department = department
    db.session.commit()


def delete(id_: int):
    """ Delete department by id. """
    delete_department = Department.query.get(id_)
    db.session.delete(delete_department)
    db.session.commit()
