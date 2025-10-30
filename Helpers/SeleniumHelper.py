from selenium import webdriver
from GettingSettings import GettingSettings
from WebDriverFactory import WebDriverFactory
from EventLoggerWin import EventLoggerWin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class SeleniumHelper:
    def __init__(self):
        self._settings = GettingSettings()
        self._factoryWebDriver = WebDriverFactory()

        self._logger = EventLoggerWin("AutoCheck")
        self._url = self._settings.getUrl()
        self._drive = self._factoryWebDriver.getDriver(option=self._settings.getBrowser())

    def execProcess(self):
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
        

