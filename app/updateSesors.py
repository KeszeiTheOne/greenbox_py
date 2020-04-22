from app.model import Sensor
from app.exception import UnexpectedType

class UpdateSensors:
    def __init__(self, sensorNotifier, sensorProviders):
        self._sensorNotifier=sensorNotifier
        self._sensorProviders=sensorProviders

    def update(self, request):
        if isinstance(request, UpdateSensorsRequest) == False:
            raise UnexpectedType()

        self._sensorNotifier.notify(self.__getSensors())

    def __getSensors(self):
        sensors=[]
        for sensorProvider in self._sensorProviders:
            sensors.append(sensorProvider.getSensor())
        self.__ensureSensors(sensors)

        return sensors

    def __ensureSensors(self, sensors):
        for sensor in sensors:
            if isinstance(sensor, Sensor) == False:
                raise UnexpectedType()

class UpdateSensorsRequest:
    pass
