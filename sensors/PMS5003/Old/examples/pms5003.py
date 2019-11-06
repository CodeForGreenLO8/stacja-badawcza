#!/usr/bin/env python

import sys
import mysql.connector
import datetime
from pms5003 import PMS5003

#if len(sys.argv) == 6
#    mysql_info = {
#        'ip'     : sys.argv[1],
#        'port'   : sys.argv[2],
#        'user'   : sys.argv[3],
#        'passwd' : sys.argv[4],
#        'db'     : sys.argv[5],
#        'table'  : sys.argv[6]
#    }
#else:
#    print('Usage: python pms5003.py <db ip> <db ip port> <db user> <db passwd> <db name> <table name>')
#    print('Example: python pms5003.py 10.0.0.172 3306 user pass db table')
#    sys.exit(1)

#db = mysql.connector.connect(
#     host   = mysql_info['ip'],     # your host, usually localhost
##    port   = mysql_info['port'],   # port - For some reason the script doesn't work with the port explicitly stated.
#     user   = mysql_info['user'],   # your username
#     passwd = mysql_info['passwd'], # your password
#     db     = mysql_info['db'])     # name of the database

# you must create a Cursor object. It will let you execute all the queries you need
#cur = db.cursor()

# get a reading
data = pms5003.read()
pm1  = data.pm_ug_per_m3(1)
pm10 = data.pm_ug_per_m3(10)
pm25 = data.pm_ug_per_m3(2.5)
print('pm1: {}\npm10: {}\npm25: {}'.format(pm1, pm10, pm25)

# Write the information to the database
#sql = "INSERT INTO {} (date, time, temperature, humidity) VALUES (%s, %s, %s, %s);".format(mysql_info['table'])
#val = (date_str, time_str, temperature, humidity)
#cur.execute(sql, val)
#db.commit()

# Close the database
#db.close()
