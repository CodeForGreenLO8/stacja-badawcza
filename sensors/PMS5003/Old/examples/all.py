#!/usr/bin/env python

from pms5003 import PMS5003

print("""all.py - Continously print all data values.

Press Ctrl+C to exit!

""")

pms5003 = PMS5003()
i = 1

try:
    while True:
        data = pms5003.read()
        print(i)
        i += 1
        print(data)

except KeyboardInterrupt:
    pass
