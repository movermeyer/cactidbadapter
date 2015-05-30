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

    # For host_table

    pprint('############################################')
    pprint('# Get Host (Default columns)')
    pprint('############################################')
    res = cacti.get_host()
    pprint(res)

    pprint('############################################')
    pprint('# Get Host (id, hostname, description.)')
    pprint('############################################')
    columns = ('id', 'hostname', 'description',)
    res = cacti.get_host(columns=columns)
    pprint(res)

    pprint('############################################')
    pprint('# Get Host (All columns.)')
    pprint('############################################')
    columns = ('*',)
    res = cacti.get_host(columns=columns)
    pprint(res)

    pprint('############################################')
    pprint('# Get Host (Only hostname and status.)')
    pprint('############################################')
    columns = ('hostname', 'status',)
    res = cacti.get_host(columns=columns)
    pprint(res)

    pprint('############################################')
    pprint('# Host table columns.')
    pprint('############################################')
    columns = cacti.host_columns()
    pprint(columns)

    ####################################################
    # Please add system.xml into your Cacti.
    # Cacti default does not have system.xml.
    # README.rst has how to add system.xml.
    ####################################################

    pprint('############################################')
    pprint('# Get SNMP sysDescr.')
    pprint('############################################')
    columns = cacti.get_sysdescr()
    pprint(columns)

    pprint('############################################')
    pprint('# Get SNMP sysName.')
    pprint('############################################')
    columns = cacti.get_sysname()
    pprint(columns)

    pprint('############################################')
    pprint('# Get SNMP sysUpTime.')
    pprint('############################################')
    columns = cacti.get_sysuptime()
    pprint(columns)

    ####################################################
    # For host_snmp_cache table.
    ####################################################

    pprint('############################################')
    pprint('# Get SNMP Cache (ifIndex values.)')
    pprint('############################################')
    condition = 'field_name = "ifIndex"'
    res = cacti.get_snmp_cache(condition=condition)
    pprint(res)

    pprint('############################################')
    pprint('# Get SNMP Cache (ifIndex and ifName values.)')
    pprint('############################################')
    condition = 'field_name = "ifIndex" or field_name = "ifName"'
    res = cacti.get_snmp_cache(condition=condition)
    pprint(res)

    pprint('############################################')
    pprint('# Get SNMP Cache (ifIndex and ifIP values.)')
    pprint('############################################')
    condition = 'field_name = "ifName" or field_name = "ifIP"'
    res = cacti.get_snmp_cache(condition=condition)
    pprint(res)

    pprint('############################################')
    pprint('# Get SNMP Cache (ifIndex and ifIP values')
    pprint('# and specified columns.)')
    pprint('############################################')
    condition = 'field_name = "ifName" or field_name = "ifIP"'
    columns = ('hostname', 'field_value', 'field_name')
    limit = 2
    res = cacti.get_snmp_cache(condition=condition,
                               columns=columns, limit=limit)
    pprint(res)

    pprint('############################################')
    pprint('# SNMP Cache available columns.')
    pprint('############################################')
    columns = cacti.host_snmp_cache_columns()
    pprint(columns)

    pprint('############################################')
    pprint('# SNMP Cache available field_names.')
    pprint('############################################')
    field_names = cacti.host_snmp_cache_field_names()
    pprint(field_names)

if __name__ == "__main__":

    main()
