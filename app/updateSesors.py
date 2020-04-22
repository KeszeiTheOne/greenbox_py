from app.model import Sensor
from app.exception import UnexpectedType

class UpdateSensors:
    def __init__(self, sensorNotifier, sensors):
        self._sensorNotifier=sensorNotifier
        self._sensors=sensors

    def update(self, request):
        if isinstance(request, UpdateSensorsRequest) == False:
            raise UnexpectedType()

        self.__ensureSensors()

        self._sensorNotifier.notify(self._sensors)

    def __ensureSensors(self):
        for sensor in self._sensors:
            if isinstance(sensor, Sensor) == False:
                raise UnexpectedType()

class UpdateSensorsRequest:
    pass
