Contributing
============

The canonical location for this repository is [on Conservancy’s
Kallithea instance](http://k.sfconservancy.org/website).  Copies of
this repository elsewhere, such as Github, are for backup purposes
only..

License
=======

The software included herein, such as the Python source files, are generally
licensed [AGPLv3](AGPLv3)-or-later.  The Javascript is a hodgepodge of
licensing, but all of it is compatible with [AGPLv3](AGPLv3)-or-later.  See
the notices at the top of each Javascript file for licensing details.

The content and text (such as the HTML files) is currently
[CC-BY-SA-3.0](CC-By-SA-3.0).

Server Configuration
====================

conservancy's webserver runs on a machine called
dogwood.sfconservancy.org, which is a standard Debian installation.

The following packages are installed to make Django and Apache work on a
squeeze install:

    $ aptitude install python-django apache2 sqlite3 python2.5-sqlite libapache2-mod-python



Django Setup
============

0. Make sure the Python module 'djangopw', with the global variable
   'djangoadmin_password' is somewhere importable in the default
   PYTHON_PATH.
