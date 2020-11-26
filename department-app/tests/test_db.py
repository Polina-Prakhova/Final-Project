""" Unittests for basic model functions. Checking Employee and Department
models. """
import unittest
from datetime import date
import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(current_path, '..')
sys.path.append(ROOT_PATH)

# pylint: disable=wrong-import-position
from models import db
from service import employee_service as es, department_service as ds
from run import create_app
# pylint: enable=wrong-import-position


class TestDB(unittest.TestCase):
    """ Test case for the CRUD methods."""
    app = create_app()

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
        """ Method runs before every test. Filling database with data. """
        with self.app.app_context():
            id_ = ds.add(name='HR', email='hr@firma.com')
            es.add(name='Mary', birthday=date(2000, 9, 22), department=id_,
                   working_since=date(2020, 1, 13), salary=30000.0)

    def tearDown(self) -> None:
        """ Method runs after every test. Remove data from database. """
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_get_all_departments(self):
        """ Test getting the list of all departments in database. """
        with self.app.app_context():
            self.assertNotEqual(ds.get_all(), [])

    def test_add_department(self):
        """ Test adding new department to database. """
        with self.app.app_context():
            ds.add(name='IT')
            self.assertEqual(len(ds.get_all()), 2)

    def test_get_existing_department(self):
        """ Test getting existing department from database. """
        with self.app.app_context():
            self.assertTrue(ds.get_by_name('HR'))

    def test_get_non_existing_department(self):
        """ Test getting non-existing department from database. """
        with self.app.app_context():
            self.assertIsNone(ds.get_by_name('ITIT'))

    def test_update_department(self):
        """ Test updating existing department in database. """
        with self.app.app_context():
            department = ds.get_by_name('HR')
            ds.update(id_=department.id,
                      name=department.name)
            self.assertNotEqual(department.email, 'hr@firma.com')

    def test_get_all_employees(self):
        """ Test getting the list of all employees in database. """
        with self.app.app_context():
            self.assertNotEqual(es.get_all(), [])

    def test_add_employee(self):
        """ Test adding new employee to database. """
        with self.app.app_context():
            id_ = ds.get_by_name('HR').id
            es.add(name='Mary', birthday=date(2000, 9, 22), department=id_,
                   working_since=date(2020, 1, 13), salary=30000.0)
            self.assertEqual(len(es.get_all()), 2)

    def test_get_existing_employee(self):
        """ Test getting existing employee from database. """
        with self.app.app_context():
            self.assertTrue(es.get_by_name('Mary'))

    def test_get_non_existing_employee(self):
        """ Test getting non-existing employee from database. """
        with self.app.app_context():
            self.assertIsNone(es.get_by_name('Polina'))

    def test_update_employee(self):
        """ Test updating existing employee in database. """
        with self.app.app_context():
            mary = es.get_by_name('Mary')
            es.update(id_=mary.id,
                      name=mary.name,
                      birthday=mary.birthday,
                      working_since=mary.working_since,
                      salary=333333,
                      department=ds.get_by_name('HR').id)
            self.assertNotEqual(mary.salary, 30000.0)

    def test_delete_data_from_tables(self):
        """ Test deleting all data from employee and department tables."""
        with self.app.app_context():
            es.delete_all()
            ds.delete_all()
            self.assertEqual(ds.get_all(), [])
            self.assertEqual(es.get_all(), [])

    def test_delete_certain_department(self):
        """ Test deleting certain department by id. """
        with self.app.app_context():
            id_ = ds.add('IT')
            ds.delete(id_)
            self.assertIsNone(ds.get_by_name('IT'))

    def test_delete_certain_employee(self):
        """ Test deleting certain employee by id. """
        with self.app.app_context():
            employee_id = es.get_by_name('Mary').id
            es.delete(employee_id)
            self.assertIsNone(es.get_by_name('Mary'))


if __name__ == '__main__':
    unittest.main()
