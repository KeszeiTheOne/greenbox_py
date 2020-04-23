#!/usr/bin/python3

import click
from app.updateSesors import UpdateSensors, UpdateSensorsRequest
from app.Emoncms.EmoncmsGateway import EmoncmsSensorGateway
from app.SensorProvider.DS18B20SensorProvider import DS18B20SensorProvider
from app.SensorProvider.DHT22HumiditySensorProvider import DHT22HumiditySensorProvider
from app.SensorProvider.DHT22TemperatureSensorProvider import DHT22TemperatureSensorProvider
from os.path import abspath, realpath
import yaml


@click.command()

def hello():
    sensors = []
    yamlSensors=None
    with open(abspath("config/sensors.yml"), 'r') as stream:
        try:
            yamlSensors=yaml.safe_load(stream)['sensors']
        except yaml.YAMLError as exc:
            print(exc)

    for yamlSensor in yamlSensors:
        if yamlSensor["type"]=="DS18B20":
            sensors.append(DS18B20SensorProvider(yamlSensor))
        elif yamlSensor["type"]=="DHT22-humidity":
            sensors.append(DHT22HumiditySensorProvider(yamlSensor))
        elif yamlSensor["type"]=="DHT22-temperature":
            sensors.append(DHT22TemperatureSensorProvider(yamlSensor))

    parameters=None
    with open(abspath("config/parameters.yml"), 'r') as stream:
        try:
            parameters=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    updater = UpdateSensors(EmoncmsSensorGateway(parameters), sensors)

    updater.update(UpdateSensorsRequest())

if __name__ == '__main__':
    hello()
