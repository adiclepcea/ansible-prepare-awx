"""
Send RaspberryPI temperature data to PostgresDB
"""
import psycopg2
from uuid import getnode as get_mac

mac = get_mac()

PG_HOST = "192.168.1.109"
PG_PASSWORD = "sensors123"
PG_DATABASE = "sensorsdb"
PG_USERNAME = "sensors"
PG_PORT = "9432"

def get_temp():
    """
    read the temperature from RaspberryPI
    """
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as infile:
        return float(infile.read()) * 0.001


try:
    CONN = psycopg2.connect("dbname='" + PG_DATABASE + "' user='" + PG_USERNAME + "' host='" + PG_HOST + "' password='" + PG_PASSWORD + "' port=" + str(PG_PORT))
    CUR = CONN.cursor()
    CUR.execute("Insert into sensordata(MacAddress, SensorValue, SensorType) values(%s, %s, %s)", (mac, get_temp(), "temp"))
    CONN.commit()
    CONN.close()
except psycopg2.Error as e:
    print "I am unable to connect to the database", e

