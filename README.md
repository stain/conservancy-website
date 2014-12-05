Contributing
============

The canonical location for this repository is
[on Gitorious](https://gitorious.org/conservancy/website).  Copies of this
repository elsewhere, such as Github, are for backup purposes only.  If you
have contributions, submit them on Gitorious.


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
