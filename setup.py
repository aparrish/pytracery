#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

setup(
    name='tracery',
    version='0.1.1',
    description="Python port of Kate Compton's "
                "tracery text generation library",
    long_description=readme + "\n\n" + history,
    author="Allison Parrish",
    author_email='allison@decontextualize.com',
    url='https://github.com/aparrish/pytracery',
    packages=[
        'tracery',
    ],
    install_requires=['inflect'],
    license="Apache License 2.0",
    zip_safe=True,
    keywords='tracery',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Artistic Software',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    test_suite='tests',
    tests_require=[]
)
