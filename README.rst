pheme.webAPIclient
==================

**Public Health EHR Message Engine (PHEME), Web API client library**

API for any client code wanting to access functionality exposed by
``pheme.webAPI``.  This generally includes archival and transfer methods.

Requirements
------------

``pheme.webAPI`` must be installed and available for this client code
to function.  The webAPI port should only allow localhost client
requests.  If connecting with remote installs, use `stunnel`_ or a
similar approach to protect all transmissions.

A pheme config file (see ``pheme.util.config``) must specify the
location of the pheme.webAPI this client library is to communicate
with.  For example::

    [WebAPI]
    host=localhost
    port=6543

Install
-------

Beyond the requirements listed above, ``pheme.webAPIclient`` is
dependent on the ``pheme.util`` module.  Although future builds may
automatically pick it up, for now, clone and build it in the same
virtual environment (or native environment) being used for
``pheme.webAPIclient``::

    git clone https://github.com/pbugni/pheme.util.git
    cd pheme.util
    ./setup.py develop
    cd ..

Then clone and build this module::

    git	clone https://github.com/pbugni/pheme.webAPIclient.git
    cd pheme.webAPIclient
    ./setup.py develop

Testing
-------

Many of the tests expect ``pheme.webAPI`` to be running (see its
documentation).  It is also strongly suggested that `in_production` be
set to `False` in the `[general]` section of the ``pheme.util.config``
file before invoking the tests.  Run the tests from the
``pheme.webAPIclient`` root as follows::

    ./setup.py test

License
-------

BSD 3 clause license - See LICENSE.txt


.. _stunnel: https://www.stunnel.org/index.html