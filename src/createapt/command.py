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
import argparse
import generator
import utils
from __init__ import __version__


def parse_options():
    parser = argparse.ArgumentParser(description='usage')
    setoption(parser, 'version')
    setoption(parser, 'rootdir')
    setoption(parser, 'codename')
    setoption(parser, 'distro')
    setoption(parser, 'section')
    setoption(parser, 'arch')
    setoption(parser, 'commands')
    args = parser.parse_args()
    return args


def setoption(parser, keyword):
    """

    Arguments:

        parser:  object of argparse
        keyword: switching keyword
    """
    if keyword == 'version':
        parser.add_argument('-V', '--version', action='version',
                            version=__version__)
    elif keyword == 'rootdir':
        parser.add_argument('-r', '--rootdir', action='store',
                            required=True,
                            help=('specify your root directory path of '
                                  'local package archive'))
    elif keyword == 'distro':
        parser.add_argument('-d', '--distro', action='store',
                            required=True,
                            help=('Debian is '
                                  'unstable, testing, stable, oldstable. '
                                  'Ubuntu is '
                                  'saucy, raring, quantal, precise, etc.'))
    elif keyword == 'codename':
        parser.add_argument('-c', '--codename', action='store',
                            help=('Debian is '
                                  'sid, jessie, wheezy, squeeze, etc. '
                                  'Ubuntu is same as distro'))
    elif keyword == 'section':
        parser.add_argument('-s', '--section', action='store',
                            required=True,
                            help=('specify some unique name. '
                                  'Debian is main, contrib, non-free. '
                                  'Ubuntu is '
                                  'main, restricted, multiverse, universe'))
    elif keyword == 'arch':
        parser.add_argument('-a', '--arch', action='store',
                            required=True,
                            help=('specified architechture name. '
                                  'amd64, armel, armhf, i386, etc.'))
    elif keyword == 'commands':
        parser.set_defaults(func=generate_archive)


def generate_archive(args):
    """

    Argument:

        args: argument object
    """
    if args.codename:
        codename = args.codename
    else:
        codename = None
    try:
        apt_gen = generator.AptArchive(args.rootdir, args.distro,
                                       args.section, args.arch, codename)
        rc, msg = apt_gen.runner()
        if rc:
            priority = 6
        else:
            priority = 5
    except (IOError, OSError) as error:
        priority = 3
        msg = error
    finally:
        utils.logging(priority, msg)


def main():
    args = parse_options()
    args.func(args)


if __name__ == '__main__':
    main()
