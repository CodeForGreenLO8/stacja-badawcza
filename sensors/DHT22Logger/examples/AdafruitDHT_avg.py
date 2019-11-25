#!/usr/bin/env python

# This script will poll the sensors multiple times, and return the results
# to stdout.

import sys
import datetime
import Adafruit_DHT
from time import sleep

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor  = sensor_args[sys.argv[1]]
    pin     = sys.argv[2]
else:
    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    print('Example: sudo ./Adafruit_DHT.py 22 4')
    sys.exit(1)

# Read sensor data multiple times and make an average
read_count  = 10
RETRY_MAX   = 15
humidity    = 0.0
temperature = 0.0
date1 = datetime.datetime.now()
print('I: AdafruitDHT_avg.py: {} | DHT22: {} readings pending...'.format(date1, read_count))
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
            print('W: AdafruitDHT_avg.py: Caught exception: \'{}\'. DHT22 reading failed.'.format(type(exception).__name__))
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
    print('I: AdafruitDHT_avg.py: {} | DHT22: Finished.'.format(date2))
    date_str = '{}-{}-{}'.format(str(date2.year), str(date2.month), str(date2.day))
    time_str = '{}:{}:{}'.format(str(date2.hour), str(date2.minute), str(date2.second))
    print('{} {} {0:0.1f} {1:0.1f}'.format(date_str, time_str, temperature, humidity))
    sys.exit(0)
else:
    raise RuntimeError('DHT22 sensor critical failure!')
    sys.exit(2)
