import time
from datetime import datetime
from Helpers.TriggerSession import TriggerSession

#We need to create the instance of Selenium because that will be our main class
trigger = TriggerSession()

if __name__ == "__main__":
    trigger.execMonitor(True)