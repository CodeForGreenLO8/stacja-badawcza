import mysql.connector
import datetime

# mySQL server information needed for establishing a connection
mysql_info = {
    'ip'     : '62.129.212.254',
    'port'   : '443',
    'user'   : '00335735_cfg',
    'passwd' : 'zmierA0D4A0zamyQbioroznorodnosci',
    'db'     : '00335735_cfg'
    'table'  : 'dht22'
}

db = mysql.connector.connect(
     host   = mysql_info['ip'],     # your host, usually localhost
     user   = mysql_info['user'],   # your username
     passwd = mysql_info['passwd'], # your password
     db     = mysql_info['db'])     # name of the database

print('Connection to 00335735_cfg established successfully.')
q = input('Insert a default reading into \'{}\' table? (y/n)').format(mysql_info['table'])

if q:
    # Default table values
    date = datetime.datetime.now();
    date_str = '{}-{}-{}'.format(str(date.year), str(date.month), str(date.day))
    time_str = '{}:{}:{}'.format(str(date.hour), str(date.minute), str(date.second))
    temperature = 20.0
    humidity = 0.35

    # Insert defaults into the table
    cur = db.cursor()
    sql = "INSERT INTO {} (date, time, temperature, humidity) VALUES (%s, %s, %s, %s);".format(mysql_info['table'])
    val = (date_str, time_str, temperature, humidity)
    cur.execute(sql, val)
    db.commit()

    # Inform the user about a successful insert
    print(date_str + ' ' + time_str)
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    print('Data inserted successfully.')

db.close()
