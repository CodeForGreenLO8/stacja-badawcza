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
read_count  = 10
RETRY_MAX   = 15
humidity    = 0.0
temperature = 0.0
date1 = datetime.datetime.now()
print('{} | DHT22: {} readings pending...'.format(date1, read_count))
# Each reading has up to RETRY_MAX chances to fail and be restarted
for i in range(read_count):
    retry_count = 0
    # Try to grab a sensor reading. Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    while retry_count < RETRY_MAX:
        try:
            h, t = Adafruit_DHT.read(sensor, pin)
            if (h == None or t == None):
                raise ValueError('DHT22 Adafruit_DHT.read() failed!')
            print('#{}\n\thumidity: {}\n\ttemperature: {}'.format(i+1, h, t))
            humidity += h
            temperature += t
            break
        except Exception as exception:
            print('Caught exception: \'{}\'. DHT22 reading failed.'.format(type(exception).__name__))
            retry_count += 1
            if retry_count < RETRY_MAX:
                print('Retrying... x{}'.format(retry_count))
            else:
                # Reading failed after all retries, reduce read_count
                read_count -= 1
            sleep(1)
    sleep(1)

if read_count > 0:
    humidity    /= read_count
    temperature /= read_count
    date2 = datetime.datetime.now()
    print('{} | DHT22: Finished.'.format(date2))
    date_str = '{}-{}-{}'.format(str(date2.year), str(date2.month), str(date2.day))
    time_str = '{}:{}:{}'.format(str(date2.hour), str(date2.minute), str(date2.second))
else:
    raise RuntimeError('DHT22 sensor critical failure!')
    exit()

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
