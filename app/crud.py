class Updater:
    def update(self, data):
        pass

class FilteringGateway:
    def filter(self, criteria):
        pass

try:
    from app.SensorProvider.DS18B20SensorProvider import DS18B20SensorProvider
except Exception as e:
    pass

try:
    from app.SensorProvider.DHT22TemperatureSensorProvider import DHT22TemperatureSensorProvider
except Exception as e:
    pass


class SensorProviderIterator():

    def __init__(self, sensorParameters):
        self.sensorParameters = sensorParameters
        self.index = 0
        self.count = len(sensorParameters)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >=self.count:
            raise StopIteration

        yamlSensor = self.sensorParameters[self.index]
        self.index+=1

        return self.__getProvider(yamlSensor)

    def __getProvider(self, yamlSensor):
        switcher = {
            "DS18B20": self.DS18B20ProviderFactory,
            "DHT22": self.DHT22TemperatureSensorProviderFactory
        }
        func = switcher.get(yamlSensor["type"], lambda: "Invalid provider")

        return func(yamlSensor)

    def DS18B20ProviderFactory(self, data):
        try:
            return DS18B20SensorProvider(data)
        except NameError as e:
            return None

    def DHT22TemperatureSensorProviderFactory(self, data):
        try:
            return DHT22TemperatureSensorProvider(data)
        except NameError as e:
            return None

class PrintGateway():

    def filter(self, criteria):
        return []

    def persistList(self, list):
        print(list)

    def find(self, id):
        pass
