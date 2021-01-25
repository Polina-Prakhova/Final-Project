""" Unittests for basic REST API functions. """
import os
import sys
import unittest
from datetime import date
import json

current_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(current_path, '..')
sys.path.append(ROOT_PATH)

# pylint: disable=wrong-import-position
from service import employee_service as es, department_service as ds
from models import db
from run import create_app
# pylint: enable=wrong-import-position


class TestDB(unittest.TestCase):
    """ Test case for the REST API."""
    app = create_app('config.TestingConfig')
    client = app.test_client()
    app.config['TESTING'] = True
    BASE = 'http://127.0.0.1:5000/'

    @classmethod
    def setUpClass(cls) -> None:
        """ Method runs once for the entire test class before tests.
        Creating connection to database. """
        with cls.app.app_context():
            db.drop_all()
            db.create_all()

    @classmethod
    def tearDownClass(cls) -> None:
        """ Method runs once for the entire test class after tests.
        Destroying connection to database. """
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self) -> None:
        with self.app.app_context():
            id_ = ds.add(name='HR', email='hr@firma.com')
            es.add(name='Mary', birthday=date(2000, 9, 22), department=id_,
                   working_since=date(2020, 1, 13), salary=30000.0)

    def tearDown(self) -> None:
        """ Method runs after every test. Remove data from database. """
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    @staticmethod
    def date_encoder(value):
        """ Encoder for date object. """
        if isinstance(value, date):
            return value.__str__()
        return value

    def test_status_code_check(self):
        """ Tests if server is running and returning HTTP code 200. """
        response = self.client.get(self.BASE)
        self.assertEqual(response.status_code, 200)

    def test_add_department(self):
        """ Test adding new department to database. """
        data = dict(name='IT', email='it@firma.com')
        response = self.client.post(self.BASE + 'api/departments',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_department(self):
        """ Test getting existing department from database. """
        response = self.client.get(self.BASE + 'api/departments/1')
        self.assertEqual(response.status_code, 200)
        department = json.loads(response.get_data(as_text=True))
        self.assertEqual(department.get('name'), 'HR')

    def test_get_all_departments(self):
        """ Test getting all existing departments from database. """
        response = self.client.get(self.BASE + 'api/departments')
        self.assertEqual(response.status_code, 200)
        department = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(department), 1)

    def test_update_department(self):
        """ Test updating existing department. """
        data = dict(id=1, name='HR')
        response = self.client.put(self.BASE + 'api/departments/1',
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        department = json.loads(response.get_data(as_text=True))
        self.assertNotEqual(department.get('email'), 'hr@firma.com')

    def test_get_non_existing_department(self):
        """ Test getting non-existing departments from database. """
        response = self.client.get(self.BASE + 'api/departments/99999')
        self.assertEqual(response.status_code, 404)

    def test_delete_department(self):
        """ Test deleting existing department from database. """
        with self.app.app_context():
            es.delete(1)
        response = self.client.delete(self.BASE + 'api/departments/1')
        self.assertEqual(response.status_code, 204)

    def test_add_employee(self):
        """ Test adding new employee to database. """
        data = dict(name='Sarah',
                    birthday=date(2000, 9, 22),
                    department=1,
                    working_since=date(2020, 1, 13),
                    salary=30000.0)
        response = self.client.post(self.BASE + 'api/employees',
                                    data=json.dumps(data,
                                                    default=self.date_encoder),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_employee(self):
        """ Test getting existing employee from database. """
        response = self.client.get(self.BASE + 'api/employees/1')
        self.assertEqual(response.status_code, 200)
        employee = json.loads(response.get_data(as_text=True))
        self.assertEqual(employee.get('name'), 'Mary')

    def test_get_all_employees(self):
        """ Test getting all existing employees from database. """
        response = self.client.get(self.BASE + 'api/employees')
        self.assertEqual(response.status_code, 200)
        employees = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(employees), 1)

    def test_update_employee(self):
        """ Test updating existing employee. """
        data = dict(id=1,
                    name='Mary',
                    birthday=date(2000, 9, 22),
                    salary=130000.0,
                    department=1,
                    working_since=date(2020, 1, 13))
        response = self.client.put(self.BASE + 'api/employees/1',
                                   data=json.dumps(data,
                                                   default=self.date_encoder),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        department = json.loads(response.get_data(as_text=True))
        self.assertEqual(department.get('salary'), 130000.0)

    def test_get_non_existing_employee(self):
        """ Test getting non-existing employee from database. """
        response = self.client.get(self.BASE + 'api/employees/99999')
        self.assertEqual(response.status_code, 404)

    def test_delete_employee(self):
        """ Test deleting existing employee from database. """
        response = self.client.delete(self.BASE + 'api/employees/1')
        self.assertEqual(response.status_code, 204)

    def test_must_return_method_not_allowed(self):
        """ Test checking right response status code for
        unacceptable HTTP methods. """
        response = self.client.post(self.BASE + 'api/departments/1')
        self.assertEqual(response.status_code, 405)
        response = self.client.put(self.BASE + 'api/departments')
        self.assertEqual(response.status_code, 405)
        response = self.client.post(self.BASE + 'api/employees/1')
        self.assertEqual(response.status_code, 405)
        response = self.client.put(self.BASE + 'api/employees')
        self.assertEqual(response.status_code, 405)

    def test_find_by_birthday(self):
        """ Test finding all employees with birthday between received dates."""
        data = dict(start=date(2000, 9, 20), end=date(2000, 9, 23))
        response = self.client.get(self.BASE + 'api/employees',
                                   data=json.dumps(data,
                                                   default=self.date_encoder),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = dict(start=date(1999, 9, 20), end=date(1999, 9, 23))
        response = self.client.get(self.BASE + 'api/employees',
                                   data=json.dumps(data,
                                                   default=self.date_encoder),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
