#!/usr/bin/env python

# This script will poll the sensors multiple times, and return the results
# to stdout.

import sys
import datetime
from pms5003 import PMS5003
from time import sleep

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
    print('{} {} {} {} {}'.format(date_str, time_str, pm1, pm10, pm25))
    sys.exit(0)
else:
    raise RuntimeError('PMS5003 sensor critical failure!')
    sys.exit(2)
