# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements/install.txt') as f:
    requirements = f.readlines()

with open('requirements/test.txt') as f:
    test_requirements = requirements + f.readlines()[1:] + ['django', ]

setup(
    name="django-consent",
    version=":versiontools:consent:",
    url='http://consent.readthedocs.org/',
    license=license,
     description="A Django app for managing permissions that a user has granted the website to do. This could be used for a number of requests, from asking the user if you can post to their twitter, or send them newsletter updates.",
    long_description=readme,
    author='Dougal Matthews',
    author_email='dougal85@gmail.com',
    setup_requires=[
        'versiontools >= 1.6',
    ],
    test_suite="runtests.runtests",
    tests_require=test_requirements,
    packages=find_packages(exclude=('docs', )),
    zip_safe=False,
    install_requires=requirements
)
