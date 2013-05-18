# -*- coding: utf-8 -*-
root_dir = '/tmp/createapt'
distro = 'unstable'
section = 'main'
arch = 'amd64'
codename = 'sid'
pool_dir = '/tmp/createapt/pool'
meta_dir = '/tmp/createapt/dists/unstable/main/binary-amd64'
override_file = '/tmp/createapt/override'
packages_file = '/tmp/createapt/dists/unstable/main/binary-amd64/Packages'
release_file = '/tmp/createapt/dists/unstable/main/Release'
override_lines = ('python-backup2swift optional python\n'
                  'python-swiftsc optional python\n')
with open('src/createapt_tests/Packages', 'rb') as f:
    packages_line = f.read()
release_lines = ('Archive: %s\nCodename: %s\n'
                 'Components: %s\nOrigin: Local\n'
                 'Label: Local\nArchitectures: %s\n' % (distro,
                                                        codename,
                                                        section,
                                                        arch))
apt_line = ('You should APT-Line as following;\n'
            '[for localhost]\n'
            'deb file:%s %s %s\n\n'
            '[for remotehost]\n'
            'deb http://localhost/pubdir/ %s %s\n'
            'Note: You should setup public directory "%s"'
            'as "/pubdir/"\n' % (root_dir, distro, section,
                                 distro, section, root_dir))
first_msg = ('Install binary package files to "%s",\n'
             'and re-run same command.' % pool_dir)
dummy_file = '/tmp/dummy'
