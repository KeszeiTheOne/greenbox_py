from app.crud import FilteringGateway
from app.model import Sensor
import requests
import json

class EmoncmsSensorGateway(FilteringGateway):
    def __init__(self, parameters):
        self.parameters=parameters
        self.sensors=[]

    def filter(self, criteria):
        response = requests.get(self.parameters["emoncms_host"] + "/input/list?apikey="+ self.parameters["emoncms_api_key"])
        self.sensors=[]
        for sensorData in response.json():
            self.sensors.append(self.__createSensor(sensorData))

        return self.sensors

    def persistList(self, list):
        sensorData={}
        for sensor in list:
            if (sensor.group in sensorData) == False:
                sensorData[sensor.group]={}
            sensorData[sensor.group][sensor.name]=sensor.value
        data=[]
        for group, asd in sensorData.items():
            qwe=[0, group]
            for name, asdasd in asd.items():
                qwe.append({name: asdasd})
            data.append(qwe)
        requests.post(self.parameters["emoncms_host"] + "/input/bulk?data="+ json.dumps(data) + "&apikey="+ self.parameters["emoncms_api_key"])

    def find(self, id):
        if isinstance(id, dict):
            for sensor in self.sensors:
                if self.__equalProperty(id, 'name', sensor) and self.__equalProperty(id, 'group', sensor):
                    return sensor
        else:
            for sensor in self.sensors:
                if id == sensor.id:
                    return sensor

        return None

    def remove(self, object):
        requests.get(self.parameters["emoncms_host"] + "/input/delete?inputid="+ object.id + "&apikey="+ self.parameters["emoncms_api_key"])

    def __equalProperty(self, criteria, property, sensor):
        return property in criteria == False or criteria[property] == getattr(sensor, property)

    def __createSensor(self, data):
        sensor = Sensor()
        sensor.id=data["id"]
        sensor.name=data["name"]
        sensor.group=data["nodeid"]
        sensor.value=data["value"]

        return sensor
