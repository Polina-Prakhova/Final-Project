""" REST API methods for Employee table"""
from flask_restful import Resource, fields, marshal_with, reqparse, inputs

from service import employee_service as es


class Department(fields.Raw):
    def format(self, value):
        return value.id


employee_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'birthday': fields.DateTime(dt_format='iso8601'),
    'department': Department,
    'working_since': fields.DateTime(dt_format='iso8601'),
    'salary': fields.Float
}

employee_args = reqparse.RequestParser()
employee_args.add_argument('name',
                           type=str,
                           help="Employee's name is required",
                           required=True)

employee_args.add_argument('birthday',
                           type=inputs.datetime_from_iso8601,
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
                           type=inputs.datetime_from_iso8601,
                           help="Date since employee working in department")


class EmployeesAPI(Resource):
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


class EmployeeAPI(Resource):
    @staticmethod
    @marshal_with(employee_fields)
    def get(id_=None):
        """ GET method, returns certain employee by id. """
        employee = es.get(id_)
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
        return es.get(id_), 201

    @staticmethod
    def delete(id_=None):
        """ DELETE method, deletes certain employee by id. """
        es.delete(id_)
        return {'result': 'Deleted'}, 200

    @staticmethod
    def post():
        """ POST method, doesn't relate to certain employee. """
        return 405
