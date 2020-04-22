from app import exception
from app import crud

class UpdateSensorAction():
    sensorUpdater=None
    def __init__(self, updater):
        self.sensorUpdater = updater

    def run(self, request):
        if isinstance(request, UpdateSensorRequest) == False:
            raise exception.UnexpectedType()
        if request.isValid() == False:
            raise exception.InvalidRequest()

        self.sensorUpdater.update(request)

class UpdateSensorRequest():
    sensorId=None
    name=None
    value=None
    def isValid(self):
        return self.sensorId != None and self.value != None
