#!/usr/bin/env python3

######################
# COPYRIGHT CFG 2019 #
######################

# ABOUT THIS SCRIPT
# This script is responsible for calling sensor-specific scripts at the right time
# and committing the results to the mySQL database.
# It needs to be running 24/7 to work properly. The polling rate can be set via the
# POLLING_RATE variable and by default is set to 300 (seconds).
# In addition, it manages the log and queue files (information about both can be found
# beneath, in their respective comment blocks).

import sys
import os
import pymysql
from time import sleep
from datetime import datetime as time

from scripthandler import *
from queuehandler import *
from loghandler import *

#########################################
#             BEGIN CONFIG              #
#########################################

# MYSQL CREDENTIALS
f = open('credentials.txt', 'r')
l = f.readlines()
MYSQL_HOST = l[0][:-1]
MYSQL_PORT = int(l[1][:-1])
MYSQL_USER = l[2][:-1]
MYSQL_PASS = l[3][:-1]
MYSQL_DB   = l[4][:-1]
l = None
f.close()

# Create script objects for every script that will be called
DHT22 = Script(
    name  = './DHT22Logger/examples/AdafruitDHT_avg.py',
    mysql = 'INSERT INTO dht22 (date, time, temperature, humidity) VALUES (%s, %s, %s, %s);',
    args  = '22 4'
)
PMS5003 = Script(
    name  = './PMS5003/Old/examples/pm25pms5003_avg.py',
    mysql = 'INSERT INTO pms5003 (date, time, pm1, pm25, pm10) VALUES (%s, %s, %s, %s, %s);',
    args  = ''
)

# Any script object from this list will be called (both at scheduled hours, and when running the script with the --debug parameter)
sensors = [
    DHT22,
    PMS5003
]

# The log file stores stdout information from running sensor scripts. This information is crucial in determining
# causes of potential failures that may occur in the future. The log file consists of 'entries'.
# Each entry consists of (in order):
#   1. Header (used to count the number of entries when traversing and truncating the log file)
#   2. Body (collective stdout information from running all scripts)
# To keep the log file from getting too bloated in size, set the LOG_PERSISTENT value. It denotes how many
# entries may be kept simultaneously. For example, setting it to 100 will delete an entry (starting from the oldest),
# when a 101th entry makes its way into the log file.
log_file = LogFile(
    name        = 'sensors.log',
    header      = '######## START ENTRY ########',
    persistence = 100
)

# If sending to database fails (for example when internet doesn't work), data will be temporarily stored in this file.
# This data will only include the bare essentials: script name and sensor readings. When the connection is back, this
# data will be sent to the database (this prevents data loss in case of a broken internet connection).
# This file doesn't have a concept of persistency like the log file does, i.e. it will store information infinitely,
# without deleting even very old entries. This is because the data is very light-weight and shouldn't pose any problems.
queue_file = QueueFile('data_queue.txt~')

POLLING_RATE = 300 # how long (in seconds) this script will wait after checking current datetime to see if scripts need to be run

#########################################
#              END CONFIG               #
#########################################

def run_full(script):
    '''Intakes a Script object, runs the script, reads its stdout and return value and commits to the db.'''
    # Run the script, get stdout and command output
    stdout, output = script.call()

    # Append stdout to the log file
    log_file.append(stdout)

    # If script finished successfully, commit to the db
    if output == 0:
        query = script.mysql
        # Every script is obligated to print its important data in the last line of stdout, parse it
        last_line = stdout.split('\n')[-1]
        values = last_line.split()
        if not mysql_push(query, values):
            # If database operation failed, push information to the external queue file
            queue_file.push('{} {}'.format(script.shortname(), last_line))
            return 1
        return 0
    else:
        # Script failed to perform even a single reading - fatal error
        print('E: master.py: run_full(): the output of sensor script {} is not 0!'.format(script.shortname()))
        return 2

def mysql_push(query, values):
    '''Runs a query on the predefined database and inserts the values `values`
    query: a string containing a mySQL query which will insert values into some table
    values: a list or tuple of the values to be inserted into the table defined in query
    '''
    try:
        db = pymysql.connect(
             host     = MYSQL_HOST,
             port     = MYSQL_PORT,
             user     = MYSQL_USER,
             password = MYSQL_PASS,
             database = MYSQL_DB
        )
        cur = db.cursor()
        log_file.append('I: master.py: mysql_push(): a connection was established successfully, querying mySQL...')
        log_file.append('\tquery = {}'.format(query))
        log_file.append('\tvalues = {}'.format(values))
        cur.execute(query, values)
        db.commit()
        db.close()
        return True
    except Exception as exception:
        # Failed to connect, return false
        errorstr = 'E: master.py: run_full(): exception occurred when connecting to mySQL: {}; saving sensor data to {}...'.format(type(exception).__name__, queue_file.name)
        log_file.append(errorstr)
        print(errorstr)
        return False

if __name__ == '__main__':
    # these flags are used to preserve information
    # about whether or not a sensor's already been used within a certain hour.
    # these flags will be reset for each new day.
    # each key represents an hour during a 24-hour day
    flags = {
        '0':  False,
        '3':  False,
        '6':  False,
        '9':  False,
        '12': False,
        '15': False,
        '18': False,
        '21': False
    }

    def reset_flags():
        for i in flags:
            flags[i] = False

    RESET_HOUR = 23             # during this hour all flags will be reset to False (last_day will also be incremented)
    last_day   = time.now().day # if the last registered day isn't the current day, flags will be reset regardless of RESET_HOUR

    def call_sensors():
        log_file.append_header(time.now())
        has_connection = True
        for s in sensors:
            output = run_full(s)
            has_connection = (output != 2) # 2 is the conventional value for "mysql_push() failed"
        while has_connection and not queue_file.empty():
            params = queue_file.top().split()
            script = tuple(filter(lambda x: x.shortname() == params[0], sensors))[0]
            if mysql_push(script.mysql, params[1:]):
                queue_file.pop()
            else:
                print('E: master.py: call_sensors(): Failed to push data to mySQL while trying to shrink the queue file.')
                has_connection = False
        log_file.truncate()
        log_file.upload()

    # debug mode can be enabled by adding a --debug or -d parameter
    # in debug mode all sensors will be activated once regardless of the time, and then the script will finish
    if len(sys.argv) == 2 and (sys.argv[1] == '--debug' or sys.argv[1] == '-d'):
        call_sensors()
        exit()
    elif len(sys.argv) > 1:
        print('Unknown parameter option(s): {}'.format(' '.join(sys.argv[1:])))
        exit()

    while (True):
        h = time.now().hour
        d = time.now().day

        # reset all flags for a new day
        if h == RESET_HOUR:
            last_day = d + 1
            reset_flags()
        elif d > last_day:
            last_day = d
            reset_flags()

        # iterate through hours to see if it's time to make a new entry
        for i in flags:
            if h == int(i) and not flags[i]:
                # activate all sensors and toggle the flag
                flags[i] = True
                call_sensors()

        # wait for the amount of time specified with POLLING_RATE
        sleep(POLLING_RATE)
