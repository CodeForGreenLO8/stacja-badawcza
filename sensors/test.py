log = None
try:
    log = open('sensors.log', 'r+')
    log.write('r+')
except:
    log = open('sensors.log', 'w+')
    log.write('w+')

while True:
    s = log.readline()[:-1]
    if s != '':
        print(s)
    else:
        print('NONEEE')
        exit()
