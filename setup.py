from setuptools import setup


fhandler = open('README.rst', 'r')
long_desc = fhandler.read()
fhandler.close()

setup(name='pytest_gae',
      version='pre-release',
      description="pytest plugin for Google App Engine",
      long_description=long_desc,
      author='Petras Zdanavicius (petraszd)',
      author_email='petras@gmail.com',
      url='http://bitbucket.org/petraszd/pytest_gae/',
      py_modules=['pytest_gae'],
      install_requires=['pytest'],
      entry_points={'pytest11': ['pytest_gae = pytest_gae']},
      license='MIT License',
      keywords='py.test pytest google app engine')
