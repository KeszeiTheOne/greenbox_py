from app.model import SensorNotifier
import requests
import json

class EmoncmsSensorNotifier(SensorNotifier):
    def __init__(self, parameters):
        self.parameters = parameters

    def notify(self, sensors):
        sensorData={}
        for sensor in sensors:
            sensorData[sensor.group][sensor.name]=sensor.value
        for group, data in sensorData:
            requests.post(self.parameters["emoncms_host"] + "/input/post?node="+ group +"&fulljson=" + json.dumps(data) + "&apikey="+ self.parameters["emoncms_api_key"])

    
