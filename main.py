import click
from app.updateSesors import UpdateSensors
from app.updateSesors import UpdateSensorsRequest
from app.Emoncms.EmoncmsSensorNotifier import EmoncmsSensorNotifier
from app.SensorProvider.DS18B20SensorProvider import DS18B20SensorProvider
from app.SensorProvider.DHT22SensorProviderHumidity import DHT22SensorProviderHumidity
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
        else if yamlSensor["type"]=="DHT22-humidity":
            sensors.append(DHT22SensorProviderHumidity(yamlSensor))
    updater = UpdateSensors(EmoncmsSensorNotifier(), sensors)

    updater.update(UpdateSensorsRequest())

if __name__ == '__main__':
    hello()
