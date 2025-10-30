from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from EventLoggerWin import EventLoggerWin
import traceback
import requests

class WebDriverFactory:
    def __init__(self):
        #I can change this definition with a json 
        self._logger = EventLoggerWin("AutoCheck")
        self._options = Options()
        self._options.add_argument("--start-maximized")
        self._service = Service(r"C:\Drivers\edgedriver_win32\msedgedriver.exe")
        self._driver = None

    def getDriver(self, option: str) -> webdriver:
        print(option)
        if option.upper() == "EDGE":
            try:
                self._driver = webdriver.Edge(service=self._service, options=self._options)

                return self._driver
            except Exception as ex:
                self._logger.throwEvent(4000001, "WARNING", ex)

                try:
                    self._driver = webdriver.Edge(driverPath)
                    return self._driver
                except Exception as ex:
                    self._logger.throwEvent(5000001, "ERROR", ex)
                    raise ValueError(ex)
                
        elif option.upper() == "FIREFOX":
            self._driver = webdriver.Firefox()
            return self._driver
        elif option.upper() == "CHROME":
            self._driver = webdriver.Chrome()
            return self._driver
        else:
            self._logger.throwEvent(5000002, "ERROR", "When we tried to get webdriver, it was choose an invalid value.")
            raise ValueError("It chose an invalid value.")

                
