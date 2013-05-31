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
import syslog
import apt
import apt_inst
import apt_pkg
from __init__ import __NAME__


def logging(priority, message):
    """

    Arguments:

        priority: syslog priority
        message:  log message
    """
    syslog.openlog(__NAME__, syslog.LOG_PID, syslog.LOG_LOCAL0)
    syslog.syslog(priority, str(message))
    syslog.closelog()
    print(message)
    if priority in range(4):
        # 0: EMERG, 1: ALERT, 2: CRIT, 3: ERR
        exit(1)
    else:
        # 4: WARNING, 5: NOTICE, 6: INFO, 7: DEBUG
        return True


def save(filepath, content):
    """Generate file

    Arguments:

        filepath: write file path
        content : string of content
    """
    with open(filepath, 'w') as f:
        f.write(content)


def check_dependency_packages(*args):
    cache = apt.Cache()
    try:
        for pkg in args:
            if not cache[pkg].is_installed:
                raise OSError('Not installed "%s" package' % pkg)
    except KeyError:
        raise OSError('Not installed "%s" package' % pkg)


def extract_meta_debpkg(pkg_path):
    """Extract tag section from control file

    Argument:

        pkg_path: debian package file path

    Return:

        tag section of "control"; Package, Priority, Section
    """
    # extract string of "control" from ".deb" file
    control_s = apt_inst.DebFile(pkg_path).control.extractdata('control')

    # convert string of "control" to Tag Object
    tag_section = apt_pkg.TagSection(control_s)

    return (tag_section.get('Package'), tag_section.get('Priority'),
            tag_section.get('Section'))
