from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class SeleniumHelper:
    def __init__(self, url):
        self._options = Options()
        self._options.add_argument("--start-maximized")
        self._service = Service(r"C:\Drivers\edgedriver_win32\msedgedriver.exe")
        self._driver = webdriver.Edge(service=self._service, options=self._options)
        self._url = url

    def execProcess(self):
        print("HOLA")

