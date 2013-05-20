import os
from setuptools import setup, find_packages

__author__ = 'uzix'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'Twisted==12.3.0',
    'thrift==0.9.0',
    'zope.interface==3.8.0',
    ]

entry_points = ''

setup(name='txsnowflake',
      version='0.1',
      description='Pheed services',
      long_description=README,
      classifiers=[
          'Programming Language :: Python',
          'Framework :: Twisted'
          ],
      author='Pheed Inc.',
      author_email='admin@pheed.com',
      packages=find_packages(where='.', exclude=['tests', 'client', 'client.txsnowflake', 'client.txsnowflake.remote']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      entry_points=entry_points,
)
