""" REST API methods for Department table"""
from flask_restful import Resource, fields, marshal_with, reqparse

from service import department_service as ds

department_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'avg_salary': fields.Float,
    'count_employees': fields.Integer,
    'email': fields.String
}

department_args = reqparse.RequestParser()
department_args.add_argument('name',
                             type=str,
                             help="Name of the department is required",
                             required=True)

department_args.add_argument('email',
                             type=str,
                             help="Email of the department is required")


class DepartmentsAPI(Resource):
    @staticmethod
    @marshal_with(department_fields)
    def get():
        """ GET method, returns department collection. """
        departments = ds.get_all()
        return departments

    @staticmethod
    @marshal_with(department_fields)
    def post():
        """ POST method, adds new department. """
        args = department_args.parse_args()
        id_ = ds.add(name=args['name'], email=args['email'])
        created_department = ds.get(id_)
        return created_department, 201

    @staticmethod
    def put():
        """ PUT method, doesn't relate to this collection. """
        return 405


class DepartmentAPI(Resource):
    @staticmethod
    @marshal_with(department_fields)
    def get(id_=None):
        """ GET method, returns certain department by id. """
        department = ds.get(id_)
        return department, 200

    @staticmethod
    @marshal_with(department_fields)
    def put(id_=None):
        """ PUT method, updates existing department by id. """
        args = department_args.parse_args()
        ds.update(id_, name=args['name'], email=args['email'])
        return ds.get(id_), 201

    @staticmethod
    def delete(id_=None):
        """ DELETE method, deletes certain department by id. """
        ds.delete(id_)
        return '', 200

    @staticmethod
    def post():
        """ POST method, doesn't relate to certain department. """
        return 405
