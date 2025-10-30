import json 
import os

'''
    Summary
        GettingSettings it help us to get json values of
        file appsetting.json at an easy way to all the project
'''

class GettingSettings:
    def __init__(self):
        self._currentFolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._nmFileSettings = "appsettings.json"

        with open(fr"{self._currentFolder}\{self._nmFileSettings}") as f:
            self._json = json.load(f)

    #Using get methods to extract the information 
    def getUrl(self) -> str:
        return self._json["Url"]
    
    def getBrowser(self) -> str:
        return self._json["Browser"]
    
    ''' 
        'Cause we could have any number of objects of services to the dribver 
        that is the reason of the needed of a for and check if exists that 
        service of the browser in the json.
    '''
    def getServices(self, option: str) -> str:
        for service in self._json["Services"]:
            if option.upper() == service:
                return service[option.upper()]
    
    def getSessionUser(self) -> str:
        return self._json["Users"]["SessionUser"]
    
    def getWorkerNumber(self) -> str:
        return self._json["Users"]["WorkerNumber"]
    
