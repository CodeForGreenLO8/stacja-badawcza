import sys
import datetime
import Adafruit_DHT

sensor = 22
pin = 4

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity = -1;
temperature = 100;
date = datetime.datetime.now();
date_str = '{}-{}-{}'.format(str(date.year), str(date.month), str(date.day))
time_str = '{}:{}:{}'.format(str(date.hour), str(date.minute), str(date.second))
print(date_str + ' ' + time_str)
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
