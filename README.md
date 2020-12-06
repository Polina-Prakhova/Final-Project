# Final-Project [![Build Status](https://travis-ci.org/Polina-Prakhova/Final-Project.svg?branch=main)](https://travis-ci.org/Polina-Prakhova/Final-Project) [![Coverage Status](https://coveralls.io/repos/github/Polina-Prakhova/Final-Project/badge.svg)](https://coveralls.io/github/Polina-Prakhova/Final-Project) 
This web application is a sort of admin dashboard in website of IT company. It includes webpages with data about departments and employees and tools to manipulate it.
# How to running project
1. Firstly, you need to install python 3 and mysql on your computer. In database create user `root` with password `root`.
2. Need to clone the project to your local computer with following command:
  ```bash
  git clone https://github.com/Polina-Prakhova/Final-Project.git
  ```
  or
  ```bash
  git clone git@github.com:Polina-Prakhova/Final-Project.git
  ```

3. (Optional) Open project folder, create virtual environment and activate it:
```bash
python3 -m venv venv
. venv/bin/activate
```

4. Run setup file to install all necessary packages:
```bash
python3 setup.py install
```

5. Now enter this command in terminal to run Gunicorn:
```bash
gunicorn -c gunicorn_config.py "department-app.wsgi:create_app()"
```
Congratulations! The application is running and available by localhost:8001 (if you haven't changed it in configs).

# URLs
Web service is available at the following URLs:
URL | HTTP method | Description
--- | --- | ---
/api/departments | GET | Returns collection of departments
/api/departments | POST | Adds new department
/api/departments/&lt;*id*&gt; | GET | Returns certain department
/api/departments/&lt;*id*&gt; | PUT | Updates certain department
/api/departments/&lt;*id*&gt; | DELETE | Deletes certain department
/api/employees | GET | Returns collection of employees
/api/employees | POST | Adds new employee
/api/employees/&lt;*id*&gt; | GET | Returns certain employee
/api/employees/&lt;*id*&gt; | PUT | Updates certain employee
/api/employees/&lt;*id*&gt; | DELETE | Deletes certain employee

<br>Web application is available at the following URLs:
URL | HTTP method | Description
--- | --- | ---
/departments | GET | Returns table with collection of departments
/departments/&lt;*id*&gt; | GET | Returns table with information about certain department
/departments/&lt;*id*&gt;/add | GET | Returns the form to create department
/departments/&lt;*id*&gt;/add | POST | Adds new department to database
/departments/&lt;*id*&gt;/update | GET | Returns the form to update certain department
/departments/&lt;*id*&gt;/update | POST | Updates information department in database
/departments/&lt;*id*&gt;/delete | POST | Deletes certain department from database
/employees | GET | Returns table with collection of employees
/employees/&lt;*id*&gt; | GET | Returns table with information about certain employees
/employees/&lt;*id*&gt;/add | GET | Returns the form to create employees
/employees/&lt;*id*&gt;/add | POST | Adds new employees to database
/employees/&lt;*id*&gt;/update | GET | Returns the form to update certain employees
/employees/&lt;*id*&gt;/update | POST | Updates information employees in database
/employees/&lt;*id*&gt;/delete | POST | Deletes certain employees from database
