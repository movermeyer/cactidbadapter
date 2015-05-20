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
        self.obj = CactiDBAdapter(user='root',
                                  password='',
                                  host='localhost',
                                  port=3306)

    def test_attrs(self):
        """test cactidbadapter."""
        # check default values
        obj = CactiDBAdapter()

        self.assertEqual(obj.database, 'cacti')
        self.assertEqual(obj.user, 'root')
        self.assertEqual(obj.password, '')
        self.assertEqual(obj.host, 'localhost')
        self.assertEqual(obj.port, 3306)
        self.assertEqual(obj.charset, 'utf8mb4')

        # check specified values
        obj = CactiDBAdapter(user='admin',
                             password='password',
                             host='localhost',
                             database='aaaaa',
                             port=12345)

        self.assertEqual(obj.database, 'aaaaa')
        self.assertEqual(obj.user, 'admin')
        self.assertEqual(obj.password, 'password')
        self.assertEqual(obj.host, 'localhost')
        self.assertEqual(obj.port, 12345)
        self.assertEqual(obj.charset, 'utf8mb4')

    def test_get_devices(self):
        """Get devices from cacti db."""
        devices = self.obj.get_devices()
        self.assertEqual(devices[0]['hostname'], '127.0.0.1')

    def test_get_snmp_cache(self):
        """Get fetched snmp values from cacti db."""
        vals = self.obj.get_snmp_cache(('ifIndex',))
        for val in vals:
            if val['field_value'] == '1':
                self.assertEqual(val['description'], 'Localhost')
                self.assertEqual(val['hostname'], '127.0.0.1')
                self.assertEqual(val['field_name'], 'ifIndex')
                self.assertEqual(val['field_value'], '1')

        vals = self.obj.get_snmp_cache(('ifIP',))
        for val in vals:
            if val['field_value'] == '10.0.2.15':
                self.assertEqual(val['description'], 'Localhost')
                self.assertEqual(val['hostname'], '127.0.0.1')
                self.assertEqual(val['field_name'], 'ifIP')
                self.assertEqual(val['field_value'], '10.0.2.15')

        vals = self.obj.get_snmp_cache(('ifIP', 'ifName'))
        for val in vals:
            if val['field_value'] == '10.0.2.15':
                self.assertEqual(val['description'], 'Localhost')
                self.assertEqual(val['hostname'], '127.0.0.1')
                self.assertEqual(val['field_name'], 'ifIP')
                self.assertEqual(val['field_value'], '10.0.2.15')

            elif val['field_value'] == 'lo':
                self.assertEqual(val['description'], 'Localhost')
                self.assertEqual(val['hostname'], '127.0.0.1')
                self.assertEqual(val['field_name'], 'ifName')
                self.assertEqual(val['field_value'], 'lo')
