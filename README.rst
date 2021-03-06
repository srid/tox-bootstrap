tox-bootstrap
=============

http://code.google.com/p/pytox/issues/detail?id=1

Getting started
---------------

::

    $ cd my_project/
    $ ls
    . .. src/ doc/ setup.py tox.ini
    $ curl http://github.com/srid/tox-bootstrap/raw/master/toxbootstrap.py -O

Instead of running "tox", now you can just run "python toxbootstrap.py" which
will take care of installing tox (if not already installed into
``.tox/toxinstall``)::

    $ python toxbootstrap.py 

If you're using Hudson_, you may also do::

    import sys
    sys.path.insert(0, '.') # sometimes necessary :/
    import toxbootstrap
    toxbootstrap.cmdline() # also accepts argv list

.. _Hudson: http://hudson-ci.org/

ToDo
----

1. Detect tox in ``$PATH`` (eg: ``C:\Python26\Scripts`` or
   ``%APPDATA%\Python\Scripts``)

2. Gracefully ignore PyPI xmlrpc downtime errors when checking for new release.
