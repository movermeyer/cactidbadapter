===================================================
cactidbadapter
===================================================

Cactidbadapter is a utility tool of python for network operators and Cacti users.
Network operators and administrators are sometimes needs to get registered data from Cacti database.
This module can get easily devices and fetched snmp polling value.

Requirements
-------------
* Python2.7, 3.4, PyPy.

Installation
-------------
Get from PyPI::

   $ pip install cactidbadapter

Get from Github ::

   $ git clone https://github.com/mtoshi/cactidbadapter
   $ cd cactidbadapter
   $ python setup.py install

Using example
--------------
Example for get_devices(). ::

    >>> from cactidbadapter import CactiDBAdapter
    >>> cacti = CactiDBAdapter(database='cacti',
    ...                        user='admin',
    ...                        password='*****',
    ...                        port=3306)
    >>> cacti.get_host()
    [{'hostname': '127.0.0.1', 'id': 1, 'description': 'Localhost'}]

Example for get_devices() with option . ::


See also
---------
* http://www.cacti.net/
