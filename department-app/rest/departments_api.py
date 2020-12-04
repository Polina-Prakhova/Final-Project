""" REST API methods for Department table"""
import logging
import os
import sys

from flask_restful import Resource, fields, marshal_with, reqparse, abort
from mysql.connector import IntegrityError

current_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(current_path, '..')
sys.path.append(ROOT_PATH)

# pylint: disable=wrong-import-position
from service import department_service as ds
# pylint: enable=wrong-import-position

logger = logging.getLogger('department_app.run')

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
    """ REST API for list of department model.
    Can get by url /api/departments.
    Includes GET, POST, DELETE and PUT methods."""

    @staticmethod
    @marshal_with(department_fields)
    def get():
        """ GET method, returns department collection. """

        logger.debug('Catch GET request by URL /api/departments.')
        departments = ds.get_all()
        return departments

    @staticmethod
    @marshal_with(department_fields)
    def post():
        """ POST method, adds new department. """

        logger.debug('Catch POST request by URL /api/departments.')
        args = department_args.parse_args()
        id_ = ds.add(name=args['name'], email=args['email'])
        created_department = ds.get(id_)
        return created_department, 201

    @staticmethod
    def put():
        """ PUT method, doesn't relate to this collection. """

        logger.debug('Catch PUT request by URL /api/departments.')
        return abort(405)


class DepartmentAPI(Resource):
    """ REST API for department model.
    Can get by url /api/department/<id>.
    Includes GET, POST, DELETE and PUT methods."""

    @staticmethod
    @marshal_with(department_fields)
    def get(id_):
        """ GET method, returns certain department by id. """

        logger.debug('Catch GET request by URL /api/departments/%i.', id_)
        try:
            department = ds.get(id_)
        except IntegrityError:
            return abort(404)
        return department, 200

    @staticmethod
    @marshal_with(department_fields)
    def put(id_=None):
        """ PUT method, updates existing department by id. """

        logger.debug('Catch PUT request by URL /api/departments/%i.', id_)
        args = department_args.parse_args()
        ds.update(id_, name=args['name'], email=args['email'])
        return ds.get(id_), 200

    @staticmethod
    def delete(id_=None):
        """ DELETE method, deletes certain department by id. """

        logger.debug('Catch DELETE request by URL /api/departments/%i.', id_)
        ds.delete(id_)
        return '', 204

    @staticmethod
    def post(id_=None):
        """ POST method, doesn't relate to certain department. """

        logger.debug('Catch POST request by URL /api/departments/%i.', id_)
        return abort(405)
