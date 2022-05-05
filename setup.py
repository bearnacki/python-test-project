from setuptools import setup

setup(
    name='python_test_project',
    version='1.0.0',
    url='https://github.com/bearnacki/python-test-project/',
    license='MIT',
    author='Patryk Biernat',
    install_requires=['pandas==1.4.2',
                      'openpyxl==3.0.9',
                      'flask-restx==0.5.1'],
    author_email='patrbiernat@gmail.com',
    description='Flask API that allow uploading an Excel file and returns a summary of provided columns ',
    packages=['python_test_project']
)