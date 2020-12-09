""" REST API methods for Department table"""
import logging
import os
import sys

from flask_restful import Resource, fields, marshal_with, reqparse, abort, \
    inputs
from sqlalchemy.exc import IntegrityError

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
                             type=inputs.regex('(?=.*@)'),
                             help="Please enter the right email.",
                             default='')


@marshal_with(department_fields)
def marshal_departments(result):
    """ Prepare result data to sending in JSON format."""
    return result


class DepartmentsAPI(Resource):
    """ REST API for list of department model.
    Can get by url /api/departments.
    Includes GET, POST, DELETE and PUT methods."""

    @staticmethod
    def get():
        """ GET method, returns department collection. """

        logger.debug('Catch GET request by URL /api/departments.')
        departments = ds.get_all()
        return marshal_departments(departments)

    @staticmethod
    def post():
        """ POST method, adds new department. """

        logger.debug('Catch POST request by URL /api/departments.')
        args = department_args.parse_args()
        try:
            id_ = ds.add(name=args['name'], email=args['email'])
            created_department = ds.get(id_)
        except IntegrityError:
            return {'message': f"Department with name {args['name']} already "
                               "exists."}, 404
        except Exception:
            return {'message': "Can't post department."}, 404
        return marshal_departments(created_department), 201

    @staticmethod
    def put():
        """ PUT method, doesn't relate to this collection. """

        logger.debug('Catch PUT request by URL /api/departments.')
        return abort(405)


class DepartmentAPI(Resource):
    """ REST API for department model.
    Can get by url /api/departments/<id>.
    Includes GET, POST, DELETE and PUT methods."""

    @staticmethod
    def get(id_):
        """ GET method, returns certain department by id. """

        logger.debug('Catch GET request by URL /api/departments/%i.', id_)
        try:
            department = ds.get(id_)
            if not department.id:
                raise Exception
        except Exception:
            logger.error('There is no department with id %i', id_)
            return {'message': f'There is no department with {id_}.'}, 404
        return marshal_departments(department)

    @staticmethod
    def put(id_=None):
        """ PUT method, updates existing department by id. """

        logger.debug('Catch PUT request by URL /api/departments/%i.', id_)
        try:
            args = department_args.parse_args()
            ds.update(id_, name=args['name'], email=args['email'])
        except Exception:
            return {'message': "Can't update department."}, 404
        return marshal_departments(ds.get(id_)), 200

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
