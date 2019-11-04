import logging
from datetime import datetime, timedelta
from serial import Serial, SerialException

from plantower import *

PMS5003 = Plantower(port='/dev/ttyAMA0')
print(str(PMS5003.read()))