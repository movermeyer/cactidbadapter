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

    def test_get_host(self):
        """Get host from cacti db."""
        hostname = '127.0.0.1'

        hosts = self.obj.get_host()
        self.assertEqual(hosts[0]['hostname'], hostname)

        hosts = self.obj.get_host(condition='hostname = "%s"' % hostname)
        self.assertEqual(hosts[0]['hostname'], hostname)

    def test_host_columns(self):
        """Check columns values."""
        columns = CactiDBAdapter.host_columns()
        self.assertEqual(len(columns), 35)

    def test_host_snmp_cache_columns(self):
        """Check columns values."""
        columns = CactiDBAdapter.host_snmp_cache_columns()
        self.assertEqual(len(columns), 42)

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

        # condition
        hostname = '127.0.0.1'
        vals = self.obj.get_snmp_cache(('ifIP', 'ifName'),
                                       condition='hostname = "%s"' % hostname)
        for val in vals:
            self.assertEqual(val['hostname'], hostname)

        # limit check
        vals = self.obj.get_snmp_cache(('ifIP',), limit=1)
        self.assertEqual(len(vals), 1)

        vals = self.obj.get_snmp_cache(('ifIP',), limit=2)
        self.assertEqual(len(vals), 2)

    def test_get_ifip(self):
        """Get fetched snmp ifIP values from cacti db."""
        vals = self.obj.get_ifip()
        for val in vals:
            if val['field_value'] == '127.0.0.1':
                self.assertEqual(val['id'], 1)
                self.assertEqual(val['hostname'], '127.0.0.1')
                self.assertEqual(val['description'], 'Localhost')
                self.assertEqual(val['field_name'], 'ifIP')
                self.assertEqual(val['oid'],
                                 '.1.3.6.1.2.1.4.20.1.2.127.0.0.1')

            if val['field_value'] == '10.0.2.15':
                self.assertEqual(val['id'], 1)
                self.assertEqual(val['hostname'], '127.0.0.1')
                self.assertEqual(val['description'], 'Localhost')
                self.assertEqual(val['field_name'], 'ifIP')
                self.assertEqual(val['oid'],
                                 '.1.3.6.1.2.1.4.20.1.2.10.0.2.15')

            if val['field_value'] == '192.168.56.2':
                self.assertEqual(val['id'], 1)
                self.assertEqual(val['hostname'], '127.0.0.1')
                self.assertEqual(val['description'], 'Localhost')
                self.assertEqual(val['field_name'], 'ifIP')
                self.assertEqual(val['oid'],
                                 '.1.3.6.1.2.1.4.20.1.2.192.168.56.2')
