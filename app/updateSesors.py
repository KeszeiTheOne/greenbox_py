from app.model import Sensor
from app.exception import UnexpectedType


class UpdateSensors:
    def __init__(self, sensorGateway, sensorProviders):
        self._sensorGateway = sensorGateway
        self._sensorProviders = sensorProviders

    def update(self, request):
        if not isinstance(request, UpdateSensorsRequest):
            raise UnexpectedType()
        filteredSensors = self._sensorGateway.filter({})
        sensors = self.__getSensors()
        self.__removeSensors(self.__getUnusedSensors(sensors, filteredSensors))

        self._sensorGateway.persistList(sensors)

    def __getSensors(self):
        sensors = []
        for sensorProvider in self._sensorProviders:
            if sensorProvider is None:
                continue
            providedsensors = sensorProvider.getSensors()
            for sensor in providedsensors:
                findSensor = self._sensorGateway.find({
                    'name': sensor.name,
                    'group': sensor.group
                })

                if findSensor is not None and sensor is not None:
                    if (findSensor.value * float(0.9)) > float(sensor.value) or (findSensor.value * float(1.1)) < float(
                            sensor.value):
                        sensorOne = sensorProvider.getSensorByName(sensor.name)
                        sensorTwo = sensorProvider.getSensorByName(sensor.name)
                        sensor.value = (float(sensor.value) + float(sensorOne.value) + float(sensorTwo.value)) / 3

                sensors.append(sensor)
        self.__ensureSensors(sensors)

        return sensors

    def __ensureSensors(self, sensors):
        for sensor in sensors:
            if not isinstance(sensor, Sensor):
                raise UnexpectedType()

    def __getUnusedSensors(self, sensors, filteredSensors):
        unusedSensors = []
        for filteredSensor in filteredSensors:
            if not self.__existSensor(filteredSensor, sensors):
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
