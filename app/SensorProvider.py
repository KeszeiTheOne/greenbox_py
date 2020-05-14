from app.model import SensorProvider
import Adafruit_DHT
from app.model import Sensor
from sensor import DS18B20
from bmp280 import BMP280

class DHT22SensorProvider(SensorProvider):
    def __init__(self, sensorData):
        self.sensorData=sensorData

    def getSensors(self):
        sensors=[]

        DHT_SENSOR = Adafruit_DHT.DHT22
        DHT_PIN = self.sensorData["pio"]
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            sensors.append(self.__createSensor("temperature", temperature))
            sensors.append(self.__createSensor("humidity", humidity))
        else:
            print("Failed to retrieve data from humidity sensor")

        return sensors

    def getSensorByName(self, name):
        for sensor in self.getSensors():
            if sensor.name == name:
                return sensor

        return None

    def __createSensor(self, type, value):
        sensor=Sensor()
        sensor.name = self.sensorData["name"]+"-"+type
        sensor.group = self.sensorData["group"]
        sensor.value = "{0:0.1f}".format(value)

        return sensor

class DS18B20SensorProvider(SensorProvider):
    def __init__(self, sensorData):
        self.sensorData=sensorData

    def getSensors(self):
        sensor=Sensor()
        ds = DS18B20(self.sensorData["code"])
        t = ds.temperature()  # read temperature
        sensor.name=self.sensorData["name"]
        sensor.group = self.sensorData["group"]
        sensor.value=t.C

        return [sensor]

    def getSensorByName(self, name):
        return self.getSensors()[0]

class BMP280SensorProvider(SensorProvider):

    def __init__(self, sensorData):
        self.sensorData=sensorData

    def getSensors(self):
        sensors=[]
        bus = SMBus(1)
        bmp280 = BMP280(i2c_dev=bus)
        if "config" in self.sensorData:
            if "read" in self.sensorData["config"]:
                for readConfig in self.sensorData["config"]:
                    if readConfig == "temperature":
                        sensors.append(self.__createSensor("temperature", bmp280.get_temperature()))
                    elif readConfig == "pressure":
                        sensors.append(self.__createSensor("pressure", bmp280.get_pressure()))

        return sensors

    def __createSensor(self, type, value):
        sensor=Sensor()
        sensor.name = self.sensorData["name"]+"-"+type
        sensor.group = self.sensorData["group"]
        sensor.value = "{:05.2f}".format(value)

        return sensor

    def getSensorByName(self, name):
        for sensor in self.getSensors():
            if sensor.name == name:
                return sensor

        return None
