class ModelDummy():
    def __init__(self):
        pass

from app.crud import Updater

class UpdaterSpy(Updater):

    updatedData=[]

    def update(self, data):
        self.updatedData.append(data)
