class Sensor:
    id=None
    name=None
    value=None
    group=None

class SensorNotifier:
    def notify(self, sensors):
        pass

class SensorProvider:
    def getSensors(self):
        pass
    def getSensorByName(self, name):
        pass

class SensorIterator:

    def __init__(self, sensorProviders):
        self._sensorProviders=sensorProviders
        self._index=0

    def __next__(self):
        if self._index in self._sensorProviders:
            sensorProvider = self._sensorProviders[self._index]
            self._index+=1
            return sensorProvider.getSensor()
        return null
