# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

license = ""
#with open('LICENSE') as f:
#    license = f.read()

setup(
    name='nbbrief_utils',
    version='0.1.0',
    description='Utilities for creating small nbbrief pages and site.',
    long_description=readme,
    author='Brian Klahn',
    author_email='k1+nbbrief_utils@klahnpages.net',
    url='https://github.com/bdklahn/nbbrief_utils',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'ipywidgets',
        'papermill',
        'voila-gridstack',
    ],
)
