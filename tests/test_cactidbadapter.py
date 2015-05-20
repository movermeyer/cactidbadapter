# -*- coding: utf-8 -*-

"""UnitTests for cactidbadapter."""

import unittest
from cactidbadapter import CactiDBAdapter


class UnitTests(unittest.TestCase):

    """Class UnitTests.

    Unit test for cactidbadapter.

    """

    def setUp(self):
        """Setup."""
        self.obj = CactiDBAdapter(database='cacti',
                                  user='root',
                                  password='password',
                                  host='localhost',
                                  port=3306)

    def test_attrs(self):
        """test cactidbadapter."""
        self.assertEqual(self.obj.database, 'cacti')
        self.assertEqual(self.obj.user, 'root')
        self.assertEqual(self.obj.password, 'password')
        self.assertEqual(self.obj.host, 'localhost')
        self.assertEqual(self.obj.port, 3306)
        self.assertEqual(self.obj.charset, 'utf8mb4')

    def test_get_devices(self):
        """Get devices from cacti db."""
        devices = self.obj.get_devices()
        self.assertEqual(devices[0]['hostname'], '127.0.0.1')

    def test_get_snmp_cache(self):
        """Get fetched snmp values from cacti db."""
        vals = self.obj.get_snmp_cache(('ifIndex',))
        self.assertEqual(vals[0]['description'], 'Localhost')
        self.assertEqual(vals[0]['hostname'], '127.0.0.1')
        self.assertEqual(vals[0]['field_name'], 'ifIndex')
        self.assertEqual(vals[0]['field_value'], '1')

        vals = self.obj.get_snmp_cache(('ifIP',))
        self.assertEqual(vals[0]['description'], 'Localhost')
        self.assertEqual(vals[0]['hostname'], '127.0.0.1')
        self.assertEqual(vals[0]['field_name'], 'ifIP')
        self.assertEqual(vals[0]['field_value'], '10.0.2.15')

        vals = self.obj.get_snmp_cache(('ifIP', 'ifName'))
        self.assertEqual(vals[0]['description'], 'Localhost')
        self.assertEqual(vals[0]['hostname'], '127.0.0.1')
        self.assertEqual(vals[0]['field_name'], 'ifIP')
        self.assertEqual(vals[0]['field_value'], '10.0.2.15')

        self.assertEqual(vals[3]['description'], 'Localhost')
        self.assertEqual(vals[3]['hostname'], '127.0.0.1')
        self.assertEqual(vals[3]['field_name'], 'ifName')
        self.assertEqual(vals[3]['field_value'], 'lo')
