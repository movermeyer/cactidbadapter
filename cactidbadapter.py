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
                Default is 'root'.
            :password (str): user password.
                Default is ''.
            :host (str): MySQL host name.
                Default is 'localhost'.
            :port (int): MySQL connect port.
                Default is 3306.
            :database (str): MySQL connect DB name.
                Default is 'cacti'.
            :charset(str): MySQL connect DB name.
                Default is 'utf8mb4'.

        """
        self.user = kwargs.get('user', 'root')
        self.password = kwargs.get('password', '')
        self.host = kwargs.get('host', 'localhost')
        self.database = kwargs.get('database', 'cacti')
        self.port = kwargs.get('port', 3306)
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
        """Execute SQL.

        Args:

            :sql (str): SQL string.

        Returns:

            :list: SQL result.

        """
        res = None

        self.connect()

        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()

        self.close()

        return res

    def get_host(self, columns=None):
        """Get cacti db registered devices.

        Args:

            :columns (list optional): Specifying display columns.
                Default is '['id', 'hostname', 'description',]'.

                Please see available column names with
                    this method "host_columns()".

        Returns:

            :list (of dict): Return nodes list of dictionary.

        Using example:

            Default columns are 'id, hostname, description' ::

                >>> obj.get_host()
                [{u'id': 1, u'hostname': u'NODE1',
                  u'description': u'test node.'}]

            Specified all columns. ::

                >>> obj.get_host(columns=['*'])
                [{u'id': 1, u'hostname': u'NODE1', ...... }]

            Same with default columns. ::

                >>> obj.get_host(columns=['id',
                                          'hostname',
                                          'description'])
                [{u'id': 1, u'hostname': u'NODE1',
                  u'description': u'test node.'}]

            Specified 'id, hostname, status' columns. ::

                >>> obj.get_host(columns=['id',
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

    def get_snmp_cache(self, field_names, columns=None, limit=None):
        """Get from "host_snmp_cache" table.

        Args:

            :field_names (list): Specifying display field_names.

            :columns (list optional): Specifying display columns.
                Default is "('id', 'hostname', 'description',
                             'field_name', 'field_value', 'oid')".

                Please see available column names with
                    this method "host_snmp_cache_columns()".

            :limit (int): limit value(integer).
                Default is None.

        Returns:

            :list (of dict): Return fetched snmp values list of dictionary.

        """
        if columns is None:
            columns = ('id', 'hostname', 'description',
                       'field_name', 'field_value', 'oid')

        if limit is None:
            limit = ''
        else:
            limit = 'limit %d' % limit

        condition = " or ".join(
            ['field_name = "%s"' % field_name for field_name in field_names])

        sql = " ".join([
            'select',
            ', '.join(columns),
            'from host left join host_snmp_cache',
            'on host.id = host_snmp_cache.host_id',
            'where %s' % condition,
            limit,
        ])

        return self.request(sql)

    def get_ifip(self, columns=None, limit=None):
        """Get ifIP values from "host_snmp_cache" table.

        Args:

            :columns (list optional): Specifying display columns.
                Default is "('id', 'hostname', 'description',
                             'field_name', 'field_value', 'oid')".

                Please see available column names with
                    this method "host_snmp_cache_columns()".

            :limit (int): limit value(integer).
                Default is None.

        Returns:

            :list (of dict): Return fetched snmp values list of dictionary.

        """
        return self.get_snmp_cache(('ifIP',), columns=columns, limit=limit)

    @staticmethod
    def host_columns():
        """Available Columns.

        Returns:

            :list (of str): Return host table column values.

        """
        return ('availability',
                'availability_method',
                'avg_time',
                'cur_time',
                'description',
                'device_threads',
                'disabled',
                'failed_polls',
                'host_template_id',
                'hostname',
                'id',
                'max_oids',
                'max_time',
                'min_time',
                'notes',
                'ping_method',
                'ping_port',
                'ping_retries',
                'ping_timeout',
                'snmp_auth_protocol',
                'snmp_community',
                'snmp_context',
                'snmp_password',
                'snmp_port',
                'snmp_priv_passphrase',
                'snmp_priv_protocol',
                'snmp_timeout',
                'snmp_username',
                'snmp_version',
                'status',
                'status_event_count',
                'status_fail_date',
                'status_last_error',
                'status_rec_date',
                'total_polls',)

    @staticmethod
    def host_snmp_cache_columns():
        """Available Columns.

        Returns:

            :list (of str): Return host_snmp_cache table column values.

        """
        return ('availability',
                'availability_method',
                'avg_time',
                'cur_time',
                'description',
                'device_threads',
                'disabled',
                'failed_polls',
                'field_name',
                'field_value',
                'host_id',
                'host_template_id',
                'hostname',
                'id',
                'max_oids',
                'max_time',
                'min_time',
                'notes',
                'oid',
                'ping_method',
                'ping_port',
                'ping_retries',
                'ping_timeout',
                'present',
                'snmp_auth_protocol',
                'snmp_community',
                'snmp_context',
                'snmp_index',
                'snmp_password',
                'snmp_port',
                'snmp_priv_passphrase',
                'snmp_priv_protocol',
                'snmp_timeout',
                'snmp_username',
                'snmp_version',
                'snmp_query_id',
                'status',
                'status_event_count',
                'status_fail_date',
                'status_last_error',
                'status_rec_date',
                'total_polls',)
