from setuptools import find_packages, setup
import os


cur_path = os.path.dirname(os.path.realpath(__file__))
requirements = cur_path + '/requirements.txt'
install_requires = []
if os.path.isfile(requirements):
    with open(requirements) as f:
        install_requires = f.read().splitlines()

requirements = cur_path + '/requirements-dev.txt'
if os.path.isfile(requirements):
    with open(requirements) as f:
        install_requires.append(f.read().splitlines())


setup(
    name='Final-Project',
    version='1.0.0',
    author='Polina Prakhova',
    packages=find_packages(exclude=('department-app/tests*')),
    install_requires=install_requires
)
