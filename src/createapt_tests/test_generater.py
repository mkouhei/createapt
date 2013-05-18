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
import createapt.generator as g
import createapt.utils as u
import test_vars as v


class GeneratorTests(unittest.TestCase):

    def setUp(self):
        self.a1 = g.AptArchive(v.root_dir, v.distro, v.section,
                               v.arch, v.codename)
        self.a2 = g.AptArchive(v.root_dir, v.distro, v.section, v.arch)

    def test__init__(self):
        self.assertFalse(self.a1.is_firstly)
        self.assertEqual(self.a1.root_dir, v.root_dir)
        self.assertEqual(self.a1.distro, v.distro)
        self.assertEqual(self.a1.section, v.section)
        self.assertEqual(self.a1.arch, v.arch)
        self.assertEqual(self.a1.codename, v.codename)
        self.assertEqual(self.a2.codename, v.distro)
        self.assertEqual(self.a2.codename, v.distro)
        self.assertEqual(self.a1.pool_dir, v.pool_dir)
        self.assertEqual(self.a1.meta_dir, v.meta_dir)
        self.assertEqual(self.a1.override_file, v.override_file)
        self.assertEqual(self.a1.packages_file, v.packages_file)
        self.assertEqual(self.a1.release_file, v.release_file)

    @unittest.expectedFailure
    def test_makedir_archive_fail(self):
        self.a1.makedir_archive()

    def test_makedir_archive(self):
        os.mkdir(self.a1.root_dir)
        self.a1.makedir_archive()
        self.assertTrue(self.a1.is_firstly)
        os.removedirs(self.a1.meta_dir)
        os.removedirs(self.a1.pool_dir)

    def test_generate_override_empty(self):
        os.mkdir(self.a1.root_dir)
        self.a1.makedir_archive()
        self.assertEqual(self.a1.generate_override(), '')
        os.removedirs(self.a1.meta_dir)
        os.removedirs(self.a1.pool_dir)

    def test_generate_override(self):
        os.mkdir(self.a1.root_dir)
        self.a1.makedir_archive()
        [shutil.copy(deb, v.pool_dir)
         for deb in glob.glob('src/createapt_tests/*.deb')]
        self.assertEqual(self.a1.generate_override(), v.override_lines)
        [os.remove(deb) for deb
         in glob.glob(os.path.join(v.pool_dir, '*.deb'))]
        os.removedirs(self.a1.meta_dir)
        os.removedirs(self.a1.pool_dir)

    def test_generate_packages(self):
        os.mkdir(self.a1.root_dir)
        self.a1.makedir_archive()
        [shutil.copy(deb, v.pool_dir)
         for deb in glob.glob('src/createapt_tests/*.deb')]
        u.save(v.override_file, self.a1.generate_override())
        self.assertEqual(self.a1.generate_packages(), v.packages_line)
        [os.remove(deb) for deb
         in glob.glob(os.path.join(v.pool_dir, '*.deb'))]
        os.remove(v.override_file)
        os.removedirs(self.a1.meta_dir)
        os.removedirs(self.a1.pool_dir)

    def test_generate_release(self):
        self.assertEqual(self.a1.generate_release(), v.release_lines)

    def test_generate_aptline(self):
        self.assertEqual(self.a1.generate_aptline(), v.apt_line)

    def test_runner_firstly(self):
        os.mkdir(self.a1.root_dir)
        self.assertEqual(self.a1.runner(),
                         (False, v.first_msg))
        os.removedirs(self.a1.meta_dir)
        os.removedirs(self.a1.pool_dir)

    def test_runner_secondly(self):
        os.mkdir(self.a1.root_dir)
        self.a1.runner()
        [shutil.copy(deb, v.pool_dir)
         for deb in glob.glob('src/createapt_tests/*.deb')]
        self.assertEqual(self.a2.runner(),
                         (True, v.apt_line))
        [os.remove(deb) for deb
         in glob.glob(os.path.join(v.pool_dir, '*.deb'))]
        os.remove(v.override_file)
        os.remove(v.packages_file)
        os.remove(v.release_file)
        os.removedirs(self.a1.meta_dir)
        os.removedirs(self.a1.pool_dir)
