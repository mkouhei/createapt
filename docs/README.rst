==================================================
 createapt is generating private packages archive
==================================================

This tools is generating the metadata necessary for private package APT archive.
This is a tool similar to createrepo command to yum / rpm.
It is a wrapper for "dpkg-scanpackages" command in practice.
Specify the parameters required by the option,
you can automatically create a local package archive.

similar packages are as follows;

* reprepro
* mini-dinstall


Requirements
------------

* Debian system or Debian-derived system
* Python 2.7
* python-apt
* dpkg-dev

Setup
-----

This depends on python-apt.
So firstly you must install "python-apt".::

  $ sudo apt-get install python-apt dpkg-dev

Then you install this software.::

  $ git clone https://github.com/mkouhei/createapt
  $ cd createapt
  $ sudo python setup.py install

or::

  $ sudo pip install createapt

or::

  $ wget http://www.palmtb.net/deb/c/python-createapt_x.x-x_all.deb
  $ sudo dpkg -i python-createapt_x.x-x_all.deb

Development
-----------

Firstly copy pre-commit hook script.::

  $ cp -f utils/pre-commit.txt .git/hooks/pre-commit

Debian systems
^^^^^^^^^^^^^^

Next install python 2.7 later, and python-apt, dpkg-dev, py.test, pep8. Debian GNU/Linux Sid system as follows,::

  $ sudo apt-geet install python python-apt dpkg-dev python-pytest pep8

Then checkout "devel" branch for development, commit your changes. Before pull request, execute git rebase.


Usage
-----

#. Make root directory of local archive.
#. Choose Debian distribution, architecture, and decise unique name of section. For example;
   * distribution: unstable
   * architecture: amd64
   * section: mycustom
#. Run the "createapt" command once first.::

     $ createapt -r /path/to/rootpath -d unstable -s mycustom -a amd64

#. Copy Debian binary package files(\*.deb) to /path/to/rootpath/pool/.
#. Run the "createapt" command with same options as a first time first.::

     $ createapt -r /path/to/rootpath -d unstable -s mycustom -a amd64

See also
--------

* `HowToSetupADebianRepository <http://wiki.debian.org/HowToSetupADebianRepository>`_
* `python-apt v0.8.0 documentation <http://apt.alioth.debian.org/python-apt-doc/index.html>`_
* `2.2 How to use APT locally <http://www.debian.org/doc/manuals/apt-howto/ch-basico.html#s-dpkg-scanpackages>`_
* `6.4.11 Local package archive <http://qref.sourceforge.net/Debian/reference/ch-package.en.html#s-local>`_
* `Debian Repository HOWTO (Obsolete Documentation) <http://www.debian.org/doc/manuals/repository-howto/repository-howto.en.html>`_


