"""
Send RaspberryPI temperature data to PostgresDB
"""
import psycopg2

def get_temp():
    """
    read the temperature from RaspberryPI
    """
    return 40.11

PG_HOST = "localhost"
PG_PASSWORD = "sensors123"
PG_DATABASE = "sensorsdb"
PG_USERNAME = "sensors"
PG_PORT = 9432




try:
    CONN = psycopg2.connect("dbname='" + PG_DATABASE + "' user='" + PG_USERNAME +
                            "' host='" + PG_HOST + "' password='" + PG_PASSWORD +
                            "' port=" + str(PG_PORT))
    CUR = CONN.cursor()
    CUR.execute("Insert into sensordata(MacAddress, SensorValue, SensorType) values(%s, %s, %s)",
                ("ssss", get_temp(), "temp"))
    CONN.commit()
    CONN.close()
    print "Gata"
except psycopg2.Error as e:
    print "I am unable to connect to the database", e
