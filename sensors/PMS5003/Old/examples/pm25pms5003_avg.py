#!/usr/bin/env python

# This script will ONCE poll the sensors, and simply send the result
# to the mySQL database, which needs to be specified in the parameters.

# This script is the initial product of experimentation, the actual script
# that gets called by master.py performs multiple readings and sends average
# data to the database, so that the results are more reliable and stable.

import sys
import mysql.connector
import datetime
from pms5003 import PMS5003

if len(sys.argv) == 7:
    mysql_info = {
        'ip'     : sys.argv[1],
        'port'   : sys.argv[2],
        'user'   : sys.argv[3],
        'passwd' : sys.argv[4],
        'db'     : sys.argv[5],
        'table'  : sys.argv[6]
    }
else:
    print('Usage: python pms5003.py <db ip> <db ip port> <db user> <db passwd> <db name> <table name>')
    print('Example: python pms5003.py 10.0.0.172 3306 user pass db table')
    sys.exit(1)

# Get a reading
pms5003 = PMS5003()
try:
    data = pms5003.read()
    pm1  = data.pm_ug_per_m3(1)
    pm10 = data.pm_ug_per_m3(10)
    pm25 = data.pm_ug_per_m3(2.5)
except Exception as exception:
    print('Caught exception: \'{}\'. PMS5003 reading failed.'.format(type(exception).__name__))
    exit()

db = mysql.connector.connect(
     host   = mysql_info['ip'],     # your host, usually localhost
#    port   = mysql_info['port'],   # port - For some reason the script doesn't work with the port explicitly stated.
     user   = mysql_info['user'],   # your username
     passwd = mysql_info['passwd'], # your password
     db     = mysql_info['db'])     # name of the database

# You must create a Cursor object. It will let you execute all the queries you need
cur = db.cursor()

# Get current date and time
date = datetime.datetime.now();
date_str = '{}-{}-{}'.format(str(date.year), str(date.month), str(date.day))
time_str = '{}:{}:{}'.format(str(date.hour), str(date.minute), str(date.second))

# Print the reading to stdout
print('{}:\n\tpm1: {}\n\tpm10: {}\n\tpm25: {}'.format(date, pm1, pm10, pm25))

# Write the information to the database
sql = "INSERT INTO {} (date, time, pm1, pm25, pm10) VALUES (%s, %s, %s, %s, %s);".format(mysql_info['table'])
val = (date_str, time_str, pm1, pm25, pm10)
cur.execute(sql, val)
db.commit()

# Close the database
db.close()
