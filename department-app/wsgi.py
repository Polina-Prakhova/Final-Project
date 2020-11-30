""" WSGI entry point. """
import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)

# pylint: disable=wrong-import-position
from run import create_app
# pylint: enable=wrong-import-position

if __name__ == '__main__':
    """ Creates app and runs it. """
    app = create_app()
    app.run()
