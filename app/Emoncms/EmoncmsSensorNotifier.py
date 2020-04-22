from app.model import SensorNotifier

class EmoncmsSensorNotifier(SensorNotifier):
    def notify(self, sensors):
        print(sensors)
