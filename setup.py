from setuptools import setup


with open('README.rst', 'r') as f:
    long_desc = f.read()

setup(name='pytest_gae',
      version='pre-release',
      description="py.test plugin for google app engine",
      long_description=long_desc,
      author='Petras Zdanavicius (petraszd)',
      author_email='petras@gmail.com',
      #url='',
      py_modules=['pytest_gae'],
      install_requires=['pytest'],
      entry_points={'pytest11': ['pytest_gae = pytest_gae']},
      license='MIT License',
      keywords='py.test pytest google app engine')
