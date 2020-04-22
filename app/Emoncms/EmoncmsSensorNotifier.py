from app.model import SensorNotifier

class EmoncmsSensorNotifier(SensorNotifier):
    def notify(self, sensors):
        for sensor in sensors:
            print(sensor.name)
            print(sensor.value)
