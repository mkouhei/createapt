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
import unittest
import sys
import os.path
import shutil
import glob
sys.path.append(os.path.abspath('src'))
import createapt.utils as u
import test_vars as v


class UtilsTests(unittest.TestCase):

    def test_logging(self):
        for i in range(4, 8):
            self.assertTrue(u.logging(i, "test of createapt.utils.logging()"))

    def test_save(self):
        u.save(v.dummy_file, 'dummy')
        self.assertTrue(os.path.isfile(v.dummy_file))
        with open(v.dummy_file, 'r') as f:
            self.assertEqual(f.read(), 'dummy')
        os.remove(v.dummy_file)

    def test_check_dependency_packages(self):
        self.assertRaises(OSError, u.check_dependency_packages, 'dummy')

    def test_check_dependency_packages_not_installed(self):
        self.assertRaises(OSError, u.check_dependency_packages,
                          'installation-guide-s390x')

    def test_extract_meta_debpkg(self):
        self.assertTupleEqual(('python-swiftsc', 'optional', 'python'),
                              u.extract_meta_debpkg(('src/createapt_tests'
                                                     '/python-swiftsc'
                                                     '_0.2.1-1_all.deb')))
