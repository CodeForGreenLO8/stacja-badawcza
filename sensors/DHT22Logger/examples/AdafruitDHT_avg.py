#!/usr/bin/env python

# This script will ONCE poll the sensors, and simply send the result
# to the mySQL database, which needs to be specified in the parameters.

# This script is the initial product of experimentation, the actual script
# that gets called by master.py performs multiple readings and sends average
# data to the database, so that the results are more reliable and stable.

import sys
import mysql.connector
import datetime
import Adafruit_DHT
from time import sleep

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

if len(sys.argv) == 9 and sys.argv[1] in sensor_args:
    sensor  = sensor_args[sys.argv[1]]
    pin     = sys.argv[2]
    mysql_info = {
        'ip'     : sys.argv[3],
        'port'   : sys.argv[4],
        'user'   : sys.argv[5],
        'passwd' : sys.argv[6],
        'db'     : sys.argv[7],
        'table'  : sys.argv[8]
    }
else:
    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number> <db ip> <db ip port> <db user> <db passwd> <db name> <table name>')
    print('Example: sudo ./Adafruit_DHT.py 2302 4 10.0.0.172 3306 user pass db table - Read from an AM2302 connected to GPIO pin #4, insert entry to table with given db credentials')
    sys.exit(1)

# Read sensor data multiple times and make an average
READING_COUNT = 10
humidity      = 0.0
temperature   = 0.0
date1 = datetime.datetime.now()
print('{} | DHT22: {} readings pending...'.format(date1, READING_COUNT))
for i in range(READING_COUNT):
    date_str = '{}-{}-{}'.format(str(date.year), str(date.month), str(date.day))
    time_str = '{}:{}:{}'.format(str(date.hour), str(date.minute), str(date.second))
    # Try to grab a sensor reading. Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    h, t= Adafruit_DHT.read_retry(sensor, pin)
    humidity += h
    temperature += t
    sleep(1)
humidity    /= READING_COUNT
temperature /= READING_COUNT
date2 = datetime.datetime.now()
print('{} | DHT22: Finished.'.format(date2))

db = mysql.connector.connect(
     host   = mysql_info['ip'],     # your host, usually localhost
#    port   = mysql_info['port'],   # port - For some reason the script doesn't work with the port explicitly stated.
     user   = mysql_info['user'],   # your username
     passwd = mysql_info['passwd'], # your password
     db     = mysql_info['db'])     # name of the database

# you must create a Cursor object. It will let you execute all the queries you need
cur = db.cursor()

# Write the information to the database
sql = "INSERT INTO {} (date, time, temperature, humidity) VALUES (%s, %s, %s, %s);".format(mysql_info['table'])
val = (date_str, time_str, temperature, humidity)
cur.execute(sql, val)
db.commit()

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')

# Close the database
db.close()
