#!/usr/bin/python3

import click
from app.updateSesors import UpdateSensors, UpdateSensorsRequest
from app.Emoncms.EmoncmsGateway import EmoncmsSensorGateway
from os.path import abspath, realpath
from app.crud import SensorProviderIterator
from app.crud import PrintGateway
import yaml


@click.command()
@click.option('-t', '--type', 'type', default="emoncms")


def hello(type):
    sensors = []
    yamlSensors=None
    with open(abspath("config/sensors.yml"), 'r') as stream:
        try:
            yamlSensors=yaml.safe_load(stream)['sensors']
        except yaml.YAMLError as exc:
            print(exc)

    sensors = SensorProviderIterator(yamlSensors)

    gateway=None
    if type == "emoncms":
        parameters=None
        with open(abspath("config/parameters.yml"), 'r') as stream:
            try:
                parameters=yaml.safe_load(stream)
                gateway=EmoncmsSensorGateway(parameters)
            except yaml.YAMLError as exc:
                print(exc)
    elif type == "print":
        gateway=PrintGateway()

    updater = UpdateSensors(gateway, sensors)

    updater.update(UpdateSensorsRequest())

if __name__ == '__main__':
    hello()
