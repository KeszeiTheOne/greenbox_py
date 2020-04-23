from app.model import SensorProvider
from app.model import Sensor
import Adafruit_DHT

class DHT22HumiditySensorProvider(SensorProvider):
    def __init__(self, sensorData):
        self.sensorData=sensorData

    def getSensor(self):
        sensor=Sensor()
        sensor.name = self.sensorData["name"]
        sensor.group = self.sensorData["group"]
        DHT_SENSOR = Adafruit_DHT.DHT22
        DHT_PIN = self.sensorData["pio"]
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            sensor.value="{0:0.1f}".format(humidity)
        else:
            print("Failed to retrieve data from humidity sensor")

        return sensor
