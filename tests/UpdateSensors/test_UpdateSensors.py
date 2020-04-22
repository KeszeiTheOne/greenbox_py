import unittest
from app import exception
from tests import fixture
from app import model
from app.updateSesors import UpdateSensorsRequest
from app.updateSesors import UpdateSensors

class UpdateSensorsTest(unittest.TestCase):

    sensors=[]

    sensorNotifier=None

    def setUp(self):
        self.sensorNotifier = SensorNotifierSpy()

    def test_unknownRequest(self):
        self.assertRaises(exception.UnexpectedType, self.update, fixture.ModelDummy)

    def test_unknownSensor(self):
        self.sensors.append(fixture.ModelDummy)
        self.assertRaises(exception.UnexpectedType, self.update, self.request())

    def test_sendedSensors(self):
        self.update(self.request())

        self.assertIs(self.sensors, self.sensorNotifier.sensors)

    def update(self, request):
        UpdateSensors(self.sensorNotifier,self.sensors).update(request)



    def request(self):
        return UpdateSensorsRequest()


class SensorNotifierSpy(model.SensorNotifier):
    sensors=None
    def notify(self, sensors):
        self.sensors=sensors
