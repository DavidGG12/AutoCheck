import json 
import os

class GettingSettings:
    def __init__(self):
        self._currentFolder = os.path.dirname(os.path.abspath(__file__))
        self._nmFileSettings = "appsetting.json"

        with open(fr"{self._currentFolder}\{self._nmFileSettings}") as f:
            self._json = json.load(f)

    def getUrl(self) -> str:
        return self._json["Url"]
    
    def getBrowser(self) -> str:
        return self._json["Browser"]
    
    def getSessionUser(self) -> str:
        return self._json["Users"]["SessionNumber"]
    
    def getWorkerNumber(self) -> str:
        return self._json["Users"]["WorkerNumber"]