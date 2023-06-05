#!/usr/bin/env python

import bme680
import time


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
output = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
    sensor.data.temperature,
    sensor.data.pressure,
    sensor.data.humidity)

print('{0},{1} Ohms'.format(
    output,
    sensor.data.gas_resistance))
