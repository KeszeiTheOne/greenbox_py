import click
from app.updateSesors import UpdateSensors
from app.updateSesors import UpdateSensorsRequest
from app.Emoncms.EmoncmsSensorNotifier import EmoncmsSensorNotifier
from app.SensorProvider.DS18B20SensorProvider import DS18B20SensorProvider
from app.SensorProvider.DHT22HumiditySensorProvider import DHT22HumiditySensorProvider
from app.SensorProvider.DHT22TemperatureSensorProvider import DHT22TemperatureSensorProvider
import yaml


@click.command()

def hello():
    sensors = []
    yamlSensors=None
    with open("config/sensors.yml", 'r') as stream:
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
    with open("config/parameters.yml", 'r') as stream:
        try:
            parameters=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    updater = UpdateSensors(EmoncmsSensorNotifier(parameters), sensors)

    updater.update(UpdateSensorsRequest())

if __name__ == '__main__':
    hello()
