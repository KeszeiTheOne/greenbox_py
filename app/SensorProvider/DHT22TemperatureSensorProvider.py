from app.model import SensorProvider
import Adafruit_DHT
from app.model import Sensor

class DHT22TemperatureSensorProvider(SensorProvider):
    def __init__(self, sensorData):
        self.sensorData=sensorData

    def getSensor(self):
        sensor=Sensor()
        sensor.name = self.sensorData["name"]
        DHT_SENSOR = Adafruit_DHT.DHT22
        DHT_PIN = self.sensorData["pio"]
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            sensor.value="{1:0.1f}".format(temperature)
        else:
            print("Failed to retrieve data from humidity sensor")

        return sensor
