#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of robotframework-smtplibrary.
# https://github.io/lucamaro/robotframework-smtplibrary

# Licensed under the Apache License 2.0 license:
# http://www.opensource.org/licenses/Apache-2.0
# Copyright (c) 2016, Luca Maragnani <luca.maragnani@gmail.com>

from setuptools import setup, find_packages

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
    'unittest',
]

setup(
    name='robotframework-smtplibrary',
    version="0.1.1",
    description='A SMTP email testing library for Robot Framework',
    long_description='''
This library aims to perform common smtp operation to be used in robotframework
''',
    keywords='robot framework testing automation smtp email mail softwaretesting',
    author='Luca Maragnani',
    author_email='luca.maragnani@gmail.com',
    url='https://github.io/lucamaro/robotframework-smtplibrary',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License 2.0 License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'robotframework'
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'robotframework-smtplibrary=robotframework_smtplibrary.cli:main',
        ],
    },
)
