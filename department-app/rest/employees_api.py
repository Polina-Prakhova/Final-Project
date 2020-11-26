""" REST API methods for Employee table. """
import os
import sys

from flask_restful import Resource, fields, marshal_with, reqparse, abort

current_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(current_path, '..')
sys.path.append(ROOT_PATH)

# pylint: disable=wrong-import-position
from service import employee_service as es
# pylint: enable=wrong-import-position


class Department(fields.Raw):
    """ Custom field for values of type department in JSON. """
    def format(self, value):
        return value.id


class Date(fields.Raw):
    """ Custom field for values of type date in JSON. """
    def format(self, value):
        return str(value)


employee_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'birthday': Date,
    'department': Department,
    'working_since': Date,
    'salary': fields.Float
}

employee_args = reqparse.RequestParser()
employee_args.add_argument('name',
                           type=str,
                           help="Employee's name is required",
                           required=True)

employee_args.add_argument('birthday',
                           type=str,
                           help="Employee's birthday is required",
                           required=True)

employee_args.add_argument('salary',
                           type=float,
                           help="Salary of the employee is required",
                           required=True)

employee_args.add_argument('department',
                           type=int,
                           help="Employee's department is required",
                           required=True)
employee_args.add_argument('working_since',
                           type=str,
                           help="Date since employee working in department")


class EmployeesAPI(Resource):
    """ REST API for list of employee model.
    Can get by url /api/employees.
    Includes GET, POST, DELETE and PUT methods."""

    @staticmethod
    @marshal_with(employee_fields)
    def get():
        """ GET method, returns employee collection. """
        employees = es.get_all()
        if not employees:
            return employees, 204
        return employees, 200

    @staticmethod
    @marshal_with(employee_fields)
    def post():
        """ POST method, adds new employee. """
        args = employee_args.parse_args()
        id_ = es.add(name=args['name'],
                     birthday=args['birthday'],
                     salary=args['salary'],
                     department=args['department'],
                     working_since=args['working_since'])

        return es.get(id_), 201

    @staticmethod
    def delete():
        """ DELETE method, deletes all collection. """
        es.delete_all()
        return {'result': 'Deleted all'}, 200

    @staticmethod
    def put():
        """ PUT method, doesn't relate to this collection. """
        return abort(405)


class EmployeeAPI(Resource):
    """ REST API for employee model.
    Can get by url /api/employee/<id>.
    Includes GET, POST, DELETE and PUT methods."""

    @staticmethod
    @marshal_with(employee_fields)
    def get(id_=None):
        """ GET method, returns certain employee by id. """
        employee = es.get(id_)
        if not employee:
            return abort(404)
        return employee, 200

    @staticmethod
    @marshal_with(employee_fields)
    def put(id_=None):
        """ PUT method, updates existing employee by id. """
        args = employee_args.parse_args()
        es.update(id_=id_,
                  name=args['name'],
                  birthday=args['birthday'],
                  salary=args['salary'],
                  department=args['department'],
                  working_since=args['working_since'])
        return es.get(id_), 200

    @staticmethod
    def delete(id_=None):
        """ DELETE method, deletes certain employee by id. """
        es.delete(id_)
        return '', 204

    @staticmethod
    def post(id_=None):
        """ POST method, doesn't relate to certain employee. """
        return abort(405)
