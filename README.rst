pheme.webAPIclient
==================

Public Health EHR Message Engine (PHEME), Web API client library

API for any client code wanting to access functionality exposed on the
pheme.webAPI.  This generally includes archival and transfer methods.

See pheme.webAPI docs for more details. 

Requirements
------------

:py:class:`pheme.webAPI` must be installed and available for this
client code to function.  The webAPI port should only allow localhost
client requests.  For remote installs, use `stunnel`_ or a similar
approach to protect all transmissions.

A pheme config file (:py:class:`pheme.util.config`) must specify the
location of the pheme.webAPI this client library is to communicate
with.  For example:

.. code::
    [WebAPI]
    host=localhost
    port=6543

License
-------

BSD 3 clause license - See LICENSE.txt


.. _stunnel: https://www.stunnel.org/index.html