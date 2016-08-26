#!/usr/bin/env python
import os

from setuptools import setup, find_packages


NAME = 'jirit'


def read_file(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()

readme = read_file('README.md')
changes = ''

install_requires = [
    'jira==1.0.7',
    'PyGithub==1.27.1',
    'PyCrypto==2.6.1'
]

tests_requires = [
]


setup(
    name=NAME,
    version=1.2,
    license='BSD',

    # Packaging.
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    provides=[NAME],

    scripts=[
        'bin/jirit-show',
        'bin/jirit-deploy'
    ],

    # You can install these using the following syntax, for example:
    # $ pip install -e .[test]
    extras_require={
        'test': tests_requires,
    },
    include_package_data=True,
    zip_safe=False,

    # Metadata for PyPI.
    description='Jirit is for getting stuff from Jira and Github.',
    long_description='\n\n'.join([readme, changes]),
    author='1%Club',
    author_email='devteam@onepercentclub.com',
    platforms=['any'],
    url='https://github.com/onepercentclub/jirit-py',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
