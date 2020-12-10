""" REST API methods for Employee table. """
import logging
import os
import sys

from flask import request
from flask_restful import Resource, fields, marshal_with, reqparse, abort

current_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(current_path, '..')
sys.path.append(ROOT_PATH)

# pylint: disable=wrong-import-position
from service import employee_service as es

# pylint: enable=wrong-import-position

logger = logging.getLogger('department_app.run')


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
                           help="Date since employee working in department",
                           default='')

birthday_args = reqparse.RequestParser()
birthday_args.add_argument('start', default=None)
birthday_args.add_argument('end', default=None)


@marshal_with(employee_fields)
def marshal_employee(result):
    """ Prepare result data to sending in JSON format."""
    return result


class EmployeesAPI(Resource):
    """ REST API for list of employee model.
    Can get by url /api/employees.
    Includes GET, POST, DELETE and PUT methods."""

    @staticmethod
    def get():
        """ GET method, returns employee collection. """

        logger.debug('Catch GET request by URL /api/employees.')
        if request.get_json() is None:
            employees = es.get_all()
        else:
            args = request.get_json()
            start = args['start']
            end = args['end']
            logger.debug('Argument start is %s, end is %s.', start, end)
            employees = es.find_by_birthday(start, end)
        if not employees:
            return '', 204
        return marshal_employee(employees)

    @staticmethod
    def post():
        """ POST method, adds new employee. """

        logger.debug('Catch POST request by URL /api/employees.')
        args = employee_args.parse_args()
        try:
            id_ = es.add(name=args['name'],
                         birthday=args['birthday'],
                         salary=args['salary'],
                         department=args['department'],
                         working_since=args['working_since'])
        except Exception:
            return {'message': "Can't post employee."}, 404

        return marshal_employee(es.get(id_)), 201

    @staticmethod
    def delete():
        """ DELETE method, deletes all collection. """

        logger.debug('Catch DELETE request by URL /api/employees.')
        es.delete_all()
        return {'result': 'All employees was deleted.'}, 200

    @staticmethod
    def put():
        """ PUT method, doesn't relate to this collection. """

        logger.debug('Catch PUT request by URL /api/employees.')
        return abort(405)


class EmployeeAPI(Resource):
    """ REST API for employee model.
    Can get by url /api/employees/<id>.
    Includes GET, POST, DELETE and PUT methods."""

    @staticmethod
    def get(id_=None):
        """ GET method, returns certain employee by id. """

        logger.debug('Catch GET request by URL /api/employees/%i.', id_)
        try:
            employee = es.get(id_)
        except Exception:
            return {'message': f'Can\'t get employee with id {id_}.'}, 404
        return marshal_employee(employee), 200

    @staticmethod
    def put(id_=None):
        """ PUT method, updates existing employee by id. """

        logger.debug('Catch PUT request by URL /api/employees/%i.', id_)
        args = employee_args.parse_args()
        try:
            es.update(id_=id_,
                      name=args['name'],
                      birthday=args['birthday'],
                      salary=args['salary'],
                      department=args['department'],
                      working_since=args['working_since'])
        except Exception:
            return {'message': 'Can\'t update employee.'}, 404
        return marshal_employee(es.get(id_)), 200

    @staticmethod
    def delete(id_=None):
        """ DELETE method, deletes certain employee by id. """
        logger.debug('Catch DELETE request by URL /api/employees/%i.', id_)

        es.delete(id_)
        return '', 204

    @staticmethod
    def post(id_=None):
        """ POST method, doesn't relate to certain employee. """
        logger.debug('Catch POST request by URL /api/employees/%i.', id_)
        return abort(405)
