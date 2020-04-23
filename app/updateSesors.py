from app.model import Sensor
from app.exception import UnexpectedType

class UpdateSensors:
    def __init__(self, sensorGateway, sensorProviders):
        self._sensorGateway=sensorGateway
        self._sensorProviders=sensorProviders

    def update(self, request):
        if isinstance(request, UpdateSensorsRequest) == False:
            raise UnexpectedType()
        sensors = self.__getSensors()
        self.__removeSensors(self.__getUnusedSensors(sensors))
        self._sensorGateway.persistList(sensors)

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

    def __getUnusedSensors(self, sensors):
        unusedSensors=[]
        for filteredSensor in self._sensorGateway.filter({}):
            if self.__existSensor(filteredSensor, sensors) == False:
                unusedSensors.append(filteredSensor)

        return unusedSensors

    def __existSensor(self, filteredSensor, sensors):
        for sensor in sensors:
            if filteredSensor.name == sensor.name and filteredSensor.group == sensor.group:
                return True

        return False

    def __removeSensors(self, sensors):
        for sensor in sensors:
            self._sensorGateway.remove(sensor)

class UpdateSensorsRequest:
    pass
