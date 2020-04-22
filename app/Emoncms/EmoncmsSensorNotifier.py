from app.model import SensorNotifier
import requests
import json

class EmoncmsSensorNotifier(SensorNotifier):
    def __init__(self, parameters):
        self.parameters = parameters

    def notify(self, sensors):
        sensorData={}
        for sensor in sensors:
            sensorData[sensor.name]=sensor.value
        print(sensorData)
        #requests.post(self.parameters["emoncms_host"] + "/input/post?node=greenbox&fulljson=" + json.dumps(sensorData) + "&apikey="+ self.parameters["emoncms_api_key"], data=payload, headers=headers)
