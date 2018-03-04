===================================================
cactidbadapter
===================================================

Cactidbadapter is a utility tool of python for network operators and Cacti users.
Network operators and administrators sometimes needs to get registered data from Cacti database.
This module can get easily devices and fetched snmp polling value.

.. image:: https://secure.travis-ci.org/mtoshi/cactidbadapter.svg?branch=master
   :target: http://travis-ci.org/mtoshi/cactidbadapter
.. image:: https://coveralls.io/repos/mtoshi/cactidbadapter/badge.svg?branch=master
   :target: https://coveralls.io/r/mtoshi/cactidbadapter?branch=master
.. image:: https://img.shields.io/pypi/v/cactidbadapter.svg
   :target: https://pypi.python.org/pypi/cactidbadapter/
   :alt: Latest Version

Requirements
-------------
* Python2.7, 3.4, PyPy.

Installation
-------------
Get from PyPI ::

   $ pip install cactidbadapter

Get from Github ::

   $ git clone https://github.com/mtoshi/cactidbadapter
   $ cd cactidbadapter
   $ python setup.py install

Using example
--------------
Example for get_host(). ::

    >>> from cactidbadapter import CactiDBAdapter
    >>> cacti = CactiDBAdapter(database='cacti',
    ...                        user='admin',
    ...                        password='*****',
    ...                        port=3306)
    >>> cacti.get_host()
    [{'hostname': '127.0.0.1', 'id': 1, 'description': 'Localhost'}]

Example for get_host() hostname and description columns. ::

    >>> cacti.get_host(columns=('hostname', 'description',))
    [{'hostname': '127.0.0.1', 'description': 'Localhost'}]

Example for get_host() all columns. ::

    >>> cacti.get_host(columns=('*',))
    [{'hostname': '127.0.0.1', 'id': 1, 'description': 'Localhost', 'snmp_version': 2, 'snmp_timeout': 500, ... }]

Example for get_host() all columns and limit 1. ::

    >>> cacti.get_host(columns=('*',), limit=1)
    [{'hostname': '127.0.0.1', 'id': 1, 'description': 'Localhost', 'snmp_version': 2, 'snmp_timeout': 500, ... }]

Example for show host table columns. ::

    >>> cacti.host_columns()
    ['availability', 'availability_method', 'avg_time', 'cur_time', 'description', ... ]

Other sample is here. ::

    https://github.com/mtoshi/cactidbadapter/blob/master/samples/sample.py

SNMP system values
-------------------
Cacti doesn't have system informations with default.
If you need system values (sysDescr, sysNaem, sysUpTime ...), then you install "system.xml".

     1. For Debian/Ubuntu ::

         sudo cp utils/cacti/system.xml /usr/share/cacti/resource/snmp_queries/

     2. Add Data Queries ::

         Name: SNMP - Get System Information
         Description: SNMP System Information
         XML Path: <path_cacti>/resource/snmp_queries/system.xml
         Data Input Method: Get SNMP Data (Indexed)

     3. Add Host Templates ::

         "Left menu" > "Host Templates" > YOUR_TEMPLATE_NAME > "Associated Data Queries" > Add

         "Add Data Query": "SNMP - Get System Information" # Select and Add.

See also
---------
* http://www.cacti.net/
