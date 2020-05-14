from app.model import SensorProvider
import Adafruit_DHT
from app.model import Sensor

class DHT22TemperatureSensorProvider(SensorProvider):
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
