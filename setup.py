# -*- coding: utf-8 -*-
"""
    Copyright (C) 2013 Kouhei Maeda <mkouhei@palmtb.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
from setuptools import setup, find_packages

sys.path.insert(0, 'src')
import createapt

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python",
    "Topic :: System :: Systems Administration",
    "Topic :: System :: Archiving :: Packaging",
]

long_description = \
        open(os.path.join("docs","README.rst")).read() + \
        open(os.path.join("docs","TODO.rst")).read() + \
        open(os.path.join("docs","HISTORY.rst")).read()

requires = ['setuptools', 'python-apt']

setup(name='createapt',
      version=createapt.__version__,
      description='generates the metadata necessary for APT archive',
      long_description=long_description,
      author='Kouhei Maeda',
      author_email='mkouhei@palmtb.net',
      url='https://github.com/mkouhei/createapt',
      license=' GNU General Public License version 3',
      classifiers=classifiers,
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=requires,
      extras_require=dict(
        test=[
            'pytest',
            'pep8',
            ],
        ),
      test_suite='tests',
      tests_require=['pytest','pep8'],
      entry_points={
        "console_scripts": [
            "createapt = createapt.command:main",
            ]
        },
)
