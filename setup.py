from setuptools import setup, find_packages
import os
from os.path import join

name = 'eea.reports'
path = name.split('.') + ['version.txt']
version = open(join(*path)).read().strip()

setup(name=name,
      version=version,
      description="EEA Reports",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='eea reports publications',
      author='European Environment Agency',
      author_email='alin.voinea@eaudeweb.ro',
      url='http://reports.eea.europa.eu',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'slc.publications',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
