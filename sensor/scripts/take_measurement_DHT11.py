#!/usr/local/bin/python

import sys
import time
import Adafruit_DHT
from influxdb import InfluxDBClient

def get_readings(sensor=Adafruit_DHT.DHT11, pin=4):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity==None:
        humidity = -100.0
    if temperature==None:
        temperature=-100.0
    return [
        {
             'measurement': 'balena-sense',
             'fields': {
                 'temperature': float(temperature),
                 'pressure': float(100.0),
                 'humidity': float(humidity),
                 'air_quality_score': float(50.0)
             }
        }
    ]

# Create the database client, connected to the influxdb container, and select/create the database
influx_client = InfluxDBClient('influxdb', 8086, database='balena-sense')
influx_client.create_database('balena-sense')

while True:
    measurements = get_readings(sensor=Adafruit_DHT.DHT11, pin=4)
    influx_client.write_points(measurements)
    time.sleep(10)
