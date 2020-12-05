import os
from multiprocessing import cpu_count

current_path = os.path.dirname(os.path.abspath(__file__))
gunicorn_path = os.path.join(current_path, 'venv/bin/gunicorn')
project_path = os.path.join(current_path, 'department-app')

command = gunicorn_path
pythonpath = project_path
bind = 'localhost:8001'
workers = cpu_count() * 2 + 1
user = None

logfile = 'gunicorn.log'
loglevel = 'info'


