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
    res = cacti.get_devices()
    pprint(res)

    pprint('###################')
    pprint('# Get Devices (id, hostname, description.)')
    pprint('###################')
    res = cacti.get_devices(columns=('id', 'hostname', 'description'))
    pprint(res)

    pprint('###################')
    pprint('# Get Devices (All columns.)')
    pprint('###################')
    res = cacti.get_devices(columns=('*',))
    pprint(res)

    pprint('###################')
    pprint('# Get Devices (Only hostname and status.)')
    pprint('###################')
    res = cacti.get_devices(columns=('hostname', 'status'))
    pprint(res)

    pprint('###################')
    pprint('# Get SNMP Cache (ifIndex values.)')
    pprint('###################')
    res = cacti.get_snmp_cache(('ifIndex',))
    pprint(res)

    pprint('###################')
    pprint('# Get SNMP Cache (ifIndex and ifName values.)')
    pprint('###################')
    res = cacti.get_snmp_cache(('ifIndex', 'ifName'))
    pprint(res)

    pprint('###################')
    pprint('# Get SNMP Cache (ifIndex and ifIP values.)')
    pprint('###################')
    res = cacti.get_snmp_cache(('ifName', 'ifIP'))
    pprint(res)

    pprint('###################')
    pprint('# Get SNMP Cache (ifIndex and ifIP values')
    pprint('# and specified columns.)')
    pprint('###################')
    res = cacti.get_snmp_cache(('ifName', 'ifIP'),
                               columns=('hostname',
                                        'field_value',
                                        'field_name'))
    pprint(res)

if __name__ == "__main__":

    main()
