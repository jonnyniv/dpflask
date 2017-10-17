from setuptools import setup

setup(name='dpflask',
      version='0.1',
      description='Daily programmer flask test',
      packages=['dpflask'],
      install_requires=[
          'flask',
          'pandas'],
      test_suite='',
      setup_requires=['pytest-runner'],
      tests_require=['pytest', 'hypothesis'],
      zip_safe=False)