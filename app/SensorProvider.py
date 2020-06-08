from app.model import SensorProvider
import Adafruit_DHT
from app.model import Sensor
from sensor import DS18B20
import board
import busio
from adafruit_bmp280 import adafruit_bmp280

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
        # Create library object using our Bus I2C port
        i2c = busio.I2C(board.SCL, board.SDA)
        bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        if "config" in self.sensorData:
            if "seaLevel" in self.sensorData["config"]:
                bmp280.seaLevelhPa = self.sensorData["config"]["seaLevel"]
            if "read" in self.sensorData["config"]:
                for readConfig in self.sensorData["config"]["read"]:
                    if readConfig == "temperature":
                        sensors.append(self.__createSensor("temperature", bmp280.temperature))
                    elif readConfig == "pressure":
                        sensors.append(self.__createSensor("pressure", bmp280.pressure))

        return sensors

    def __createSensor(self, type, value):
        sensor=Sensor()
        sensor.name = self.sensorData["name"]+"-"+type
        sensor.group = self.sensorData["group"]
        sensor.value = "{%0.1f}".format(value)

        return sensor

    def getSensorByName(self, name):
        for sensor in self.getSensors():
            if sensor.name == name:
                return sensor

        return None
