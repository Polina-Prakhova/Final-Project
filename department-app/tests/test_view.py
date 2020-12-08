""" Unittests for view functions. """
import os
import sys
import unittest
from datetime import date

current_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(current_path, '..')
sys.path.append(ROOT_PATH)

# pylint: disable=wrong-import-position
from service import employee_service as es, department_service as ds
from views import employee_view as ev, department_view as dv
from models import db
from run import create_app


# pylint: enable=wrong-import-position


class TestDB(unittest.TestCase):
    """ Test case for the REST API."""
    app = create_app('config.TestingConfig')
    app.config['SERVER_NAME'] = '127.0.0.1:500'
    client = app.test_client()
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

    def test_render_template_departments_in_response_if_success(self):
        """ Tests if was rendered template departments.html after requesting
        to /departments page. Checks whether a html tag (average salary) is
        contained in response or not. """
        with self.app.app_context():
            response = dv.show_all_departments()
            self.assertIn('<td>30000.0 $</td>', response)

    def test_render_template_employees_in_response_if_success(self):
        """ Tests if was rendered template employees.html after requesting
        to /employees page. Checks whether a html tag (birthday) is contained
        in response or not. """
        with self.app.app_context():
            response = ev.show_all_employees()
            self.assertIn('<td>2000-09-22</td>', response)
            self.assertNotIn('<td>2020-01-13</td>', response)

    def test_render_template_department_in_response_if_success(self):
        """ Tests if was rendered template department.html after requesting
        to /departments/<id> page. Checks whether a html tag (email)
        is contained in response or not. """
        with self.app.app_context():
            response = dv.show_department(1)
            self.assertIn('<th>E-mail</th>', response)

    def test_render_template_employee_in_response_if_success(self):
        """ Tests if was rendered template employee.html after requesting
        to /employees/<id> page. Checks whether a html tag (working since)
        is contained in response or not. """
        with self.app.app_context():
            response = ev.show_employee(1)
            self.assertIn('<td>2020-01-13</td>', response)

    def test_render_template_department_in_response_if_error(self):
        """ Tests if logs with level 'ERROR' have been created if there is no
        department with received id and if raised exception is NotFound. """
        with self.app.app_context():
            with self.assertRaises(Exception):
                dv.show_department(111)

            self.assertLogs("An error occurred while retrieving department "
                            "with id 111", level='ERROR')

    def test_render_template_employee_in_response_if_error(self):
        """ Tests if logs with level 'ERROR' have been created if there is no
        employee with received id and if raised exception is NotFound. """
        with self.app.app_context():
            with self.assertRaises(Exception):
                ev.show_employee(111)

            self.assertLogs("Can't get employee with id 111", level='ERROR')

    def test_render_template_delete_department_if_success(self):
        """ Tests if was redirection after successful deleting. """
        with self.app.app_context():
            es.delete_all()
            response = dv.delete_department(1)
            self.assertIn(b'http://127.0.0.1:500/departments', response.data)

    def test_render_template_delete_department_if_error(self):
        """ Tests if logs with level 'ERROR' have been created if there is no
        department with received id and if raised exception is NotFound. """
        with self.app.app_context():
            with self.assertRaises(Exception):
                dv.delete_department(11)
            self.assertLogs("Can't delete department with id 11", level='ERROR')

    def test_render_template_delete_employee_if_success(self):
        """ Tests if was redirection after successful deleting employee. """
        with self.app.app_context():
            response = ev.delete_employee(1)
            self.assertIn(b'http://127.0.0.1:500/employees', response.data)

    def test_render_template_delete_employee_if_error(self):
        """ Tests if logs with level 'ERROR' have been created if there is no
        employee with received id and if raised exception is NotFound. """
        with self.app.app_context():
            with self.assertRaises(Exception):
                ev.delete_employee(11)

            self.assertLogs("Can't get employee with id 11", level='ERROR')

    def test_render_template_update_department_if_success(self):
        """ Tests if was rendered template edit_department.html after requesting
        to /departments/<id> page. Checks whether a html tag (name) is
        contained in response or not. """
        with self.app.app_context():
            with self.app.test_request_context():
                response = dv.update_department(1)
                self.assertIn('Updating department: HR', response)

    def test_render_template_update_department_if_error(self):
        """ Tests if logs with level 'ERROR' have been created if there is no
        department with received id and if raised exception is NotFound. """
        with self.app.app_context():
            with self.app.test_request_context():
                with self.assertRaises(Exception):
                    dv.update_department(11)
                self.assertLogs("Can't get department with id 11", level='ERROR')

    def test_render_template_update_employee_if_success(self):
        """ Tests if was rendered template edit_employee.html after requesting
        to /employees/<id> page. Checks whether a html tag (name) is
        contained in response or not. """
        with self.app.app_context():
            with self.app.test_request_context():
                response = ev.update_employee(1)
                self.assertIn('Updating employee: Mary', response)

    def test_render_template_update_employee_if_error(self):
        """ Tests if logs with level 'ERROR' have been created if there is no
        employee with received id and if raised exception is NotFound. """
        with self.app.app_context():
            with self.app.test_request_context():
                with self.assertRaises(Exception):
                    ev.update_employee(11)

                self.assertLogs("Can't get employee with id 11", level='ERROR')

    def test_method_post_update_department_success(self):
        """ Tests if department was updated and getting right status code. """
        new_name = 'IT'
        with self.app.app_context():
            with self.app.test_request_context(method='POST',
                                               data={'name': new_name,
                                                     'email': ''}):
                response = dv.update_department(1)
                self.assertEqual(response.status_code, 302)
            self.assertEqual(ds.get(1).name, new_name)

    def test_method_post_update_department_error(self):
        """ Tests if raised exception is NotFound while department
        updating was failed. """
        new_name = 'IT'
        with self.app.app_context():
            ds.add(new_name)
            with self.app.test_request_context(method='POST',
                                               data={'name': new_name,
                                                     'email': ''}):
                response = dv.update_department(1)
            department = ds.get(1)
            self.assertNotEqual(department.name, new_name)
            self.assertEqual(response.status_code, 302)

    def test_method_post_update_employee_success(self):
        """ Tests if employee was updated and getting right status code. """
        new_name = 'Taras'
        with self.app.app_context():
            with self.app.test_request_context \
                        (method='POST', data=dict(name=new_name,
                                                  birthday=date(2000, 9, 22),
                                                  department_name=1,
                                                  working_since=date(2020, 1,
                                                                     13),
                                                  salary=30000.0)):
                response = ev.update_employee(1)
                self.assertEqual(response.status_code, 302)
            self.assertEqual(es.get(1).name, new_name)


if __name__ == '__main__':
    unittest.main()
