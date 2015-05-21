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

    def select_query(self, columns, table, condition, limit):
        """Make Seletct SQL string.

        Args:

            :columns (list): Specifying display columns.
            :condition (str): This string is used with where condition.
            :limit (int): Limit value(integer).

        Returns:

            :list (of dict): Return fetched snmp values list of dictionary.

        """
        columns = ', '.join(columns)

        sql = [
            'select',
            columns,
            'from %s' % table]

        if condition:
            sql.append('where %s' % condition)

        if limit:
            sql.append('limit %d' % limit)

        return self.request(' '.join(sql))

    def get_host(self, columns=None, condition=None, limit=None):
        """Get cacti db registered devices.

        Args:

            :columns (list optional): Specifying display columns.
                Default is '['id', 'hostname', 'description',]'.

                Please see available column names with
                    this method "host_columns()".

            :condition (str optional): This string is used with
                where condition. Default is None.

            :limit (int optional): Limit value(integer).
                Default is None.

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

        table = 'host'
        return self.select_query(columns, table, condition, limit)

    def get_snmp_cache(self, columns=None, condition=None, limit=None):
        """Get from "host_snmp_cache" table.

        Args:

            :columns (list optional): Specifying display columns.
                Default is "('id', 'hostname', 'description',
                             'field_name', 'field_value', 'oid')".

                Please see available column names with
                    this method "host_snmp_cache_columns()".

            :condition (str optional): This string is used with
                where condition. Default is None.

            :limit (int optional): Limit value(integer).
                Default is None.

        Returns:

            :list (of dict): Return fetched snmp values list of dictionary.

        """
        if columns is None:
            columns = ('id', 'hostname', 'description',
                       'field_name', 'field_value', 'oid')

        table = ('host left join host_snmp_cache'
                 ' on host.id = host_snmp_cache.host_id')
        return self.select_query(columns, table, condition, limit)

    def host_snmp_cache_field_names(self):
        """Get field_name(s) from host_snmp_cache table."""
        field_names = []
        columns = ('field_name',)
        for val in self.get_snmp_cache(columns=columns):
            field_names.append(val['field_name'])
        _field_names = list(set(field_names))
        _field_names.sort()
        return _field_names

    def get_ifip(self, columns=None, condition=None, limit=None):
        """Get ifIP values from "host_snmp_cache" table.

        This is a wrapper method of "get_snmp_cache()".

        Args:

            :columns (list optional): Specifying display columns.
                Default is "('id', 'hostname', 'description',
                             'field_name', 'field_value', 'oid')".

                Please see available column names with
                    this method "host_snmp_cache_columns()".

            :condition (str optional): This string is used with
                where condition. Default is None.

            :limit (int optional): limit value(integer).
                Default is None.

        Returns:

            :list (of dict): Return fetched snmp values list of dictionary.

        """
        condition = 'field_name = "ifIP"'
        return self.get_snmp_cache(columns=columns,
                                   condition=condition,
                                   limit=limit)

    def host_columns(self):
        """Available host table columns.

        Returns:

            :list (of str): Return host table column values.

        """
        columns = ('*',)
        limit = 1
        record = self.get_host(columns=columns, limit=limit)[0]
        return self.get_columns(record)

    def host_snmp_cache_columns(self):
        """Available host_snmp_cache table columns.

        Returns:

            :list (of str): Return host_snmp_cache table column values.

        """
        columns = ('*',)
        limit = 1
        record = self.get_snmp_cache(columns=columns, limit=limit)[0]
        return self.get_columns(record)

    @staticmethod
    def get_columns(record):
        """Available table columns.

        Args:

            :dict (of str): One record dict.

        Returns:

            :list (of str): Return table column values.

        """
        column_names = list(record.keys())
        column_names.sort()
        return column_names
