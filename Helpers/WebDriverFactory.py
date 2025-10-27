from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

class WebDriverFactory:
    def __init__(self):
        self._options = Options()
        self._options.add_argument("--start-maximized")
        self._service = Service(r"C:\Drivers\edgedriver_win32\msedgedriver.exe")
        self._driver = None

    def getDriver(self, option):
        if option == "Edge":
            try:
                self._driver = webdriver.Edge()
                return self._driver
            except:
                
