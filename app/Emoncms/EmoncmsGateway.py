from app.crud import FilteringGateway
from app.model import Sensor
import requests
import json

class EmoncmsSensorGateway(FilteringGateway):
    def __init__(self, parameters):
        self.parameters=parameters

    def filter(self, criteria):
        response = requests.get(self.parameters["emoncms_host"] + "/input/list?apikey="+ self.parameters["emoncms_api_key"])
        sensors=[]
        for sensorData in response.json():
            sensor = Sensor()
            sensor.id=sensorData["id"]
            sensor.name=sensorData["name"]
            sensor.group=sensorData["nodeid"]
            sensor.value=sensorData["value"]
            sensors.append(sensor)

        return sensors

    def persistList(self, list):
        sensorData={}
        for sensor in list:
            if (sensor.group in sensorData) == False:
                sensorData[sensor.group]={}
            sensorData[sensor.group][sensor.name]=sensor.value
        for group, data in sensorData:
            requests.post(self.parameters["emoncms_host"] + "/input/post?node="+ group +"&fulljson=" + json.dumps(data) + "&apikey="+ self.parameters["emoncms_api_key"])

    def remove(self, object):
        requests.get(self.parameters["emoncms_host"] + "/input/delete?inputid="+ object.id + "&apikey="+ self.parameters["emoncms_api_key"])
