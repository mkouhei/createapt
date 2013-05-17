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
import os.path
import glob
import apt_inst
import apt_pkg
import apt
import subprocess


def extract_meta_debpkg(pkg_path):
    """Extract tag section from control file

    Argument:

        pkg_path: debian package file path
    """
    control_s = apt_inst.DebFile(pkg_path).control.extractdata('control')
    tag_section = apt_pkg.TagSection(control_s)
    return (tag_section.get('Package'), tag_section.get('Priority'),
            tag_section.get('Section'))


class AptArchive(object):

    def __init__(self, codename, root_dir, distro, section, arch):
        self.is_firstly = False
        self.codename = codename
        self.root_dir = root_dir
        self.distro = distro
        self.section = section
        self.arch = arch
        self.pool_dir = os.path.join(root_dir, "pool")
        self.meta_dir = os.path.join(root_dir, "dists/%s/%s/binary-%s" %
                                     (distro, section, arch))
        self.override_file = os.path.join(root_dir, 'override')
        self.packages_file = os.path.join(self.meta_dir, 'Packages')
        self.release_file = os.path.join(os.path.dirname(self.meta_dir),
                                         'Release')
        self.cache = apt.Cache()
        if self.cache['dpkg-dev']:
            raise OSError('Not installed "dpkg-dev" package')

    def makedir_archive(self):
        if not os.path.isdir(self.root_dir):
            raise IOError('No such directory "%s"' % self.root_dir)

        # put package files
        if not os.path.isdir(self.pool_dir):
            os.makedirs(self.pool_dir, 0755)
            self.is_firstly = True
        # put meta files
        if not os.path.isdir(self.meta_dir):
            os.makedirs(self.meta_dir, 0755)
            self.is_firstly = True

    def generate_packages_list(self):
        pkg_name_list = [extract_meta_debpkg(pkg)
                         for pkg in glob.glob(os.path.join(self.pool_dir,
                                                           '*.deb'))]
        # remove duplicate
        return list(set(pkg_name_list))

    def generate_override_file(self):
        packages_list_s = ''
        for l in self.generate_packages_list():
            packages_list_s += "%s %s %s\n" % l
            self.override_file_path = os.path.join(self.root_dir, 'override')
        with open(self.override_file_path, 'w') as f:
            f.write(packages_list_s)
        return True

    def generate_packages_file(self):
        stdout = subprocess.check_output(['dpkg-scanpackages',
                                          self.pool_dir,
                                          self.override_file_path,
                                          self.root_dir])
        with open(self.packages_file, 'w') as f:
            f.write(stdout)
        return True

    def generate_release_file(self):
        release_file = os.path.join(os.path.dirname(self.meta_dir), 'Release')
        content = ('Archive: %s\n'
                   'Codename: %s\n'
                   'Components: %s\n'
                   'Origin: Local\n'
                   'Label: Local\n'
                   'Architectures: %s\n') % (self.distro, self.codename,
                                             self.section, self.arch)
        with open(release_file, 'w') as f:
            f.write(content)
        return True

    def echo_aptline(self):
        apt_line = 'You should APT-Line as following;\n'
        apt_line += '[for localhost]\n'
        apt_line += 'deb file:%s %s %s\n\n' % (self.root_dir,
                                               self.distro,
                                               self.section)
        apt_line += '[for remotehost]\n'
        apt_line += 'deb http://localhost/pubdir/ %s %s\n' % (self.distro,
                                                              self.section)
        apt_line += ('Note: You should setup public directory "%s"'
                     'as "/pubdir/"\n') % self.root_dir
        return apt_line

    def runner(self):
        self.makedir_archive()
        if self.firstly:
            return (False, 'You should binary package files in "%s"'
                    % self.pool_dir)
        else:
            self.generate_override_file()
            self.generate_packages_file()
            self.generate_release_file()
            return (True, self.echo_aptline())
