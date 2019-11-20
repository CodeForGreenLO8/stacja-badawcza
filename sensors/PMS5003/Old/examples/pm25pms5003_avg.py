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
from time import sleep

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

# Read sensor data multiple times and make an average
pms5003 = PMS5003()
read_count  = 10
RETRY_MAX   = 15
pm1  = 0.0
pm10 = 0.0
pm25 = 0.0
date1 = datetime.datetime.now()
print('I: pm25pms5003_avg.py: {} | PMS5003: {} readings pending...'.format(date1, read_count))
# Each reading has up to RETRY_MAX chances to fail and be restarted
for i in range(read_count):
    retry_count = 0
    # Try to grab a sensor reading. Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    while retry_count < RETRY_MAX:
        try:
            data = pms5003.read()
            p1  = data.pm_ug_per_m3(1)
            p10 = data.pm_ug_per_m3(10)
            p25 = data.pm_ug_per_m3(2.5)
            if (p1 == None or p10 == None or p25 == None):
                raise ValueError('PMS5003 pms5003.read() failed!')
            print('#{}\n\tpm1: {}\n\tpm10: {}\n\tpm25: {}'.format(i+1, p1, p10, p25))
            pm1  += p1
            pm10 += p10
            pm25 += p25
            break
        except Exception as exception:
            print('W: pm25pms5003: Caught exception: \'{}\'. PMS5003 reading failed.'.format(type(exception).__name__))
            retry_count += 1
            if retry_count < RETRY_MAX:
                print('Retrying... x{}'.format(retry_count))
            else:
                # Reading failed after all retries, reduce read_count
                read_count -= 1
            sleep(1)
    sleep(1)

if read_count > 0:
    pm1  /= read_count
    pm10 /= read_count
    pm25 /= read_count
    date2 = datetime.datetime.now()
    print('I: pm25pms5003.py: {} | PMS5003: Finished.'.format(date2))
    date_str = '{}-{}-{}'.format(str(date2.year), str(date2.month), str(date2.day))
    time_str = '{}:{}:{}'.format(str(date2.hour), str(date2.minute), str(date2.second))
else:
    raise RuntimeError('PMS5003 sensor critical failure!')
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
print('pm1: {}\npm10: {}\npm25: {}'.format(pm1, pm10, pm25))

# Write the information to the database
sql = "INSERT INTO {} (date, time, pm1, pm25, pm10) VALUES (%s, %s, %s, %s, %s);".format(mysql_info['table'])
val = (date_str, time_str, pm1, pm25, pm10)
cur.execute(sql, val)
db.commit()

# Close the database
db.close()
