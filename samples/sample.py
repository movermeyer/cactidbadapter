# -*- coding: utf-8 -*-
"""Sample code."""


from cactidbadapter import CactiDBAdapter
from pprint import pprint


def main():
    """Main."""
    cacti = CactiDBAdapter(user='root',
                           password='',
                           host='localhost',
                           port=3306)

    pprint('###################')
    pprint('# Get Devices (Default columns)')
    pprint('###################')
    res = cacti.get_host()
    pprint(res)

    pprint('###################')
    pprint('# Get Devices (id, hostname, description.)')
    pprint('###################')
    res = cacti.get_host(columns=('id', 'hostname', 'description'))
    pprint(res)

    pprint('###################')
    pprint('# Get Devices (All columns.)')
    pprint('###################')
    res = cacti.get_host(columns=('*',))
    pprint(res)

    pprint('###################')
    pprint('# Get Devices (Only hostname and status.)')
    pprint('###################')
    res = cacti.get_host(columns=('hostname', 'status'))
    pprint(res)

    pprint('###################')
    pprint('# Get SNMP Cache (ifIndex values.)')
    pprint('###################')
    condition = 'field_name = "ifIndex"'
    res = cacti.get_snmp_cache(condition=condition)
    pprint(res)

    pprint('###################')
    pprint('# Get SNMP Cache (ifIndex and ifName values.)')
    pprint('###################')
    condition = 'field_name = "ifIndex" or field_name = "ifName"'
    res = cacti.get_snmp_cache(condition=condition)
    pprint(res)

    pprint('###################')
    pprint('# Get SNMP Cache (ifIndex and ifIP values.)')
    pprint('###################')
    condition = 'field_name = "ifName" or field_name = "ifIP"'
    res = cacti.get_snmp_cache(condition=condition)
    pprint(res)

    pprint('###################')
    pprint('# Get SNMP Cache (ifIndex and ifIP values')
    pprint('# and specified columns.)')
    pprint('###################')
    condition = 'field_name = "ifName" or field_name = "ifIP"'
    columns = ('hostname', 'field_value', 'field_name')
    limit = 2
    res = cacti.get_snmp_cache(condition=condition,
                               columns=columns, limit=limit)
    pprint(res)

if __name__ == "__main__":

    main()
