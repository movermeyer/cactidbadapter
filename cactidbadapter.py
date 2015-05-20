# -*- coding: utf-8 -*-

"""cactidbadapter.CactiDBAdapter."""

import pymysql.cursors


class CactiDBAdapter(object):

    """class CactiDBAdapter.

    Cacti DB Adapter

    """

    def __init__(self, **kwargs):
        """Initialize.

        Args:

            :user (str): user name.
            :password (str): user password.
            :host (str): MySQL host name.
            :port (int): MySQL connect port.
            :database (str): MySQL connect DB name.

        """
        self.host = kwargs['host']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.database = kwargs['database']
        self.port = kwargs['port']
        self.charset = kwargs.get('charset', 'utf8mb4')
        self.cursorclass = pymysql.cursors.DictCursor
        self.connection = None

    def connect(self):
        """Connect."""
        self.connection = pymysql.connect(host=self.host,
                                          user=self.user,
                                          passwd=self.password,
                                          db=self.database,
                                          port=self.port,
                                          charset=self.charset,
                                          cursorclass=self.cursorclass)

    def close(self):
        """Close."""
        self.connection.close()

    def request(self, sql):
        """Request."""
        res = None

        self.connect()

        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()

        self.close()

        return res

    def get_devices(self, columns=None):
        """Get cacti db registered devices.

        Returns:

            :list (of dict): Return nodes list of dictionary.


        Using example:

            Default columns are 'id, hostname, description' ::
            >>> obj.get_devices()
            [{u'id': 1, u'hostname': u'NODE1', u'description': u'test node.'}]

        Specified all columns. ::

            >>> obj.get_devices(columns=['*'])
            [{u'id': 1, u'hostname': u'NODE1', ...... }]

        Same with default columns. ::

            >>> obj.get_devices(columns=['id',
                                         'hostname',
                                         'description'])
            [{u'id': 1, u'hostname': u'NODE1', u'description': u'test node.'}]

        Specified 'id, hostname, status' columns. ::

            >>> obj.get_devices(columns=['id',
                                         'hostname',
                                         'status'])
            [{u'id': 1, u'hostname': u'NODE1', u'status': 3}]

        """
        if columns is None:
            columns = ('id', 'hostname', 'description')

        sql = " ".join([
            'select',
            ', '.join(columns),
            'from host',
        ])

        return self.request(sql)

    def get_snmp_cache(self, keywords, columns=None):
        """Get from "host_snmp_cache" table."""
        if columns is None:
            columns = ('id', 'hostname', 'description',
                       'field_name', 'field_value', 'oid')

        condition = " or ".join(
            ['field_name = "%s"' % keyword for keyword in keywords])

        sql = " ".join([
            'select',
            ', '.join(columns),
            'from host left join host_snmp_cache',
            'on host.id = host_snmp_cache.host_id',
            'where %s' % condition,
            'limit 10',
        ])

        return self.request(sql)
