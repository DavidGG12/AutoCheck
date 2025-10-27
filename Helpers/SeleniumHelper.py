from selenium import webdriver
from GettingSettings import GettingSettings
from WebDriverFactory import WebDriverFactory
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class SeleniumHelper:
    def __init__(self):
        self._settings = GettingSettings
        self._factoryWebDriver = WebDriverFactory

        self._url = self._settings.getUrl()
        self._drive = self._factoryWebDriver.getDriver(option=self._settings.getBrowser())

    def execProcess(self):
        self._drive.get("http://rh.sanborns.com.mx/web/checador")
        
        

