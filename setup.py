#!/usr/bin/env python
from setuptools import setup, find_packages

from usda_nutrition import __version__


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='django-usda-nutrition',
    version=__version__,
    packages=find_packages(exclude=('tests*',)),
    include_package_data=True,
    author='Daniel Naab',
    author_email='dan@crushingpennies.com',
    description='Django application for working with the USDA nutrition database.',
    long_description=readme(),
    url='https://github.com/danielnaab/django-usda-nutrition',
    license='BSD',
    keywords='django',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 1.9'
    ],
    test_suite='run_tests'
)
