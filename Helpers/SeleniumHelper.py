from selenium import webdriver
from Helpers.GettingSettings import GettingSettings
from Helpers.WebDriverFactory import WebDriverFactory
from Helpers.EventLoggerWin import EventLoggerWin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, datetime, time

class SeleniumHelper:
    def __init__(self):
        #Definition of instances
        self._settings = GettingSettings()
        self._factoryWebDriver = WebDriverFactory()
        self._logger = EventLoggerWin("AutoCheck")

        #Definition of settings that we going to need to define our driver
        self._url = self._settings.getUrl()
        self._drive = self._factoryWebDriver.getDriver(option=self._settings.getBrowser())
        
        #Definition of schedule that we need to execute proceess and actual time
        self._schedule = [time(8, 0), time(10, 0)]
        self._actualTime = datetime.now().time()

    def validateSchedule(self) -> bool:
        return True if(self._schedule[0] >= self._actualTime >= self._schedule[1]) else False 

    def execProcess(self) -> None:
        if not self.validateSchedule():
            return

        try:
            self._drive.get("http://rh.sanborns.com.mx/web/checador")

            # Wait for the page to be fully loaded
            WebDriverWait(self._drive, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            iframe = WebDriverWait(self._drive, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            self._drive.switch_to.frame(iframe)
            txtInput = self._drive.find_element(By.ID, "numeroEmpleado")

            txtInput.send_keys(self._settings.getWorkerNumber())
            
            self._logger.throwEvent(2000001, "INFO", "PROCESS WAS EXECUTING SUCCESSFULLY.")

            # input("Press ENTER to close Edge...")

            # self._drive.quit()
        except Exception as e:
            self._logger.throwEvent(5000003, "ERROR", e)
            raise ValueError(e)
        

