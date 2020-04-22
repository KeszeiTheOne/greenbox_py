from sensor import DS18B20
from app.model import SensorProvider
from app.model import Sensor

class DS18B20SensorProvider(SensorProvider):
    def __init__(self, sensorData):
        self.sensorData=sensorData

    def getSensor(self):
        sensor=Sensor()
        ds = DS18B20(self.sensorData["code"])
        t = ds.temperature()  # read temperature
        sensor.name=self.sensorData["name"]
        sensor.value=t.C

        return sensor
