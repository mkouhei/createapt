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
import subprocess
import utils


class AptArchive(object):

    def __init__(self, root_dir, distro, section, arch, codename=None):
        """

        Arguments:

            root_dir: specify root directory path of local package archive
            distro  : Debian's distribution; unstable, testing, stable, etc.
            section : Debian's section; main, contrib, non-free
            arch    : Debian's architecture name; amd64, armel, i386, etc.
            codename: Debian's release codename; sid, jessie, wheezy, etc.
        """
        self.is_firstly = False
        self.root_dir = root_dir
        self.distro = distro
        if codename:
            self.codename = codename
        else:
            self.codename = distro
        self.section = section
        self.arch = arch
        self.pool_dir = os.path.join(root_dir, "pool")
        self.meta_dir = os.path.join(root_dir, "dists/%s/%s/binary-%s" %
                                     (distro, section, arch))
        self.override_file = os.path.join(root_dir, 'override')
        self.packages_file = os.path.join(self.meta_dir, 'Packages')
        self.release_file = os.path.join(os.path.dirname(self.meta_dir),
                                         'Release')
        utils.check_dependency_packages('dpkg-dev')

    def makedir_archive(self):
        """
        Make directories under root directory of package archive.
        This method is executed once only.
        """
        if not os.path.isdir(self.root_dir):
            raise IOError('No such directory "%s"' % self.root_dir)

        # make directory for putting package files
        if not os.path.isdir(self.pool_dir):
            os.makedirs(self.pool_dir, 0755)
            self.is_firstly = True

        # make dierctory for putting meta files
        if not os.path.isdir(self.meta_dir):
            os.makedirs(self.meta_dir, 0755)
            self.is_firstly = True

        return

    def generate_override(self):
        """
        Generate parameters of "override" file.
        Parameters of "override" file are follows;
        <packagename> <priority> <section>
        """
        debpkg_files = glob.glob(os.path.join(self.pool_dir, '*.deb'))

        pkg_name_list = [utils.extract_meta_debpkg(pkg)
                         for pkg in debpkg_files]

        # remove duplicate with list(set(list))
        pkg_name_list_without_duplicate = list(set(pkg_name_list))

        packages_list_s = ''
        for line in pkg_name_list_without_duplicate:
            packages_list_s += "%s %s %s\n" % line

        return packages_list_s

    def generate_packages(self):
        """
        Generate content of "Packages" file with dpkg-scanpackages command.
        Need to prepare install "*.deb" files to "pool" directory.
        """
        if not os.path.isfile('/usr/bin/dpkg-scanpackages'):
            raise IOError('No such file "/usr/bin/dpkg-scanpackages"')

        # change directory
        curdir = os.path.abspath(os.path.curdir)
        os.chdir(self.root_dir)

        # execute "dpkg-scanpackages" command.
        packages_s = subprocess.check_output(['dpkg-scanpackages',
                                              'pool',
                                              self.override_file])
        os.chdir(curdir)
        return packages_s

    def generate_release(self):
        """Generate content of Release file."""
        release_s = ('Archive: %s\n'
                     'Codename: %s\n'
                     'Components: %s\n'
                     'Origin: Local\n'
                     'Label: Local\n'
                     'Architectures: %s\n') % (self.distro, self.codename,
                                               self.section, self.arch)
        return release_s

    def generate_aptline(self):
        """Return notification message of apt-line."""
        apt_line = ('You should APT-Line as following;\n'
                    '[for localhost]\n'
                    'deb file:%s %s %s\n\n'
                    '[for remotehost]\n'
                    'deb http://localhost/pubdir/ %s %s\n'
                    'Note: You should setup public directory "%s"'
                    'as "/pubdir/"\n' % (self.root_dir,
                                         self.distro,
                                         self.section,
                                         self.distro,
                                         self.section,
                                         self.root_dir))
        return apt_line

    def runner(self):
        """Running methods of generating archive."""
        self.makedir_archive()
        if self.is_firstly:
            return (False, ('Install binary package files to "%s",\n'
                            'and re-run same command.' % self.pool_dir))
        else:
            utils.save(self.override_file, self.generate_override())
            utils.save(self.packages_file, self.generate_packages())
            utils.save(self.release_file, self.generate_release())
            return (True, self.generate_aptline())
