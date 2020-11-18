from sqlalchemy import func
from models.models import DepartmentInfo, Department, Employee, db


def get_all():
    return DepartmentInfo.query.all()


def add(name: str):
    avg_salary = db.session.query(
        func.avg(Employee.salary)
    ).filter(
        Employee.department_id == Department.id
    ).filter(
        Department.name == name
    ).scalar()

    count_employees = db.session.query(
        func.count(Employee.id)
    ).filter(
        Employee.department_id == Department.id
    ).filter(
        Department.name == name
    ).scalar()

  #  new_department_info = DepartmentInfo(name)
  #  db.session.add(new_department_info)
  #  db.session.commit()

