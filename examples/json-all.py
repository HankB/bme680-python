#!/usr/bin/env python3

'''
Script intended to read the BME680 and output the results in
JSON format in order to publish to my personal Homeassistant
setup. A typical command line would be:

json-all.sh | mosquitto_pub -l -h mqtt -t "HA/"$(/usr/bin/hostname)"/kitchen/temp_humidity_press_VOC"

Left as an exercise for the student to add to cron.

TODO: Add instrictions for installation w/out running the Pimoroni install script.
'''

import bme680
import time
import json

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Up to 10 heater profiles can be configured, each
# with their own temperature and duration.
# sensor.set_gas_heater_profile(200, 150, nb_profile=1)
# sensor.select_gas_heater_profile(1)
# sensor.get_sensor_data() # prime sensor
# time.sleep(0.1)
# sensor.get_sensor_data() # prime sensor
# time.sleep(0.1)
repeat_count=0
while not (sensor.get_sensor_data() and sensor.data.heat_stable):
    time.sleep(0.1)
    repeat_count += 1
    if repeat_count > 5:
        print("sensor.get_sensor_data() unsuccessful")
        exit(1)

'''
output = '{0:.2f} °C,{1:.2f} hPa,{2:.2f} %RH {3:.2f} Ohms'.format(
    sensor.data.temperature,
    sensor.data.pressure,
    sensor.data.humidity,
    sensor.data.gas_resistance)
print(output)
'''
timeStamp = int(time.time())
payload_json = json.dumps({ "t": timeStamp, 
                            "temp":round(sensor.data.temperature/5.0*9.0+32.0, 1),
                            "pressure":round(sensor.data.pressure, 2),
                            "humidity":round(sensor.data.humidity, 2),
                            "VOC_R":int(sensor.data.gas_resistance+0.5),
                            "repeats:":repeat_count})
print(payload_json)
