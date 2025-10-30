import win32evtlogutil
import win32evtlog

'''
    Summary
        EventLoggerWin, this class is to have a logger when 
        the project will be a exe. 'Cause we won't be able
        to see the console so, the logger we going to put 
        on Windows Log Viewer.
'''
class EventLoggerWin:
    def __init__(self, appName: str):
        #We need a App name, so this will be a constant that we can see on Log Viewer.
        self.APPNAME = appName

    def throwEvent(self, eventID: int, typeEvent: str, message: chr) -> None:
        try:
            typeEventLog: win32evtlog

            if typeEvent.upper() == "INFO":
                typeEventLog = win32evtlog.EVENTLOG_INFORMATION_TYPE
            elif typeEvent.upper() == "SUCCESS":
                typeEventLog = win32evtlog.EVENTLOG_SUCCESS
            elif typeEvent.upper() == "WARNING":
                typeEventLog = win32evtlog.EVENTLOG_WARNING_TYPE
            elif typeEvent.upper() == "ERROR":
                typeEventLog = win32evtlog.EVENTLOG_ERROR_TYPE
            else:
                raise ValueError("Option chose isn't a validate value.")

            win32evtlogutil.ReportEvent(
                appName=self.APPNAME,
                eventID=eventID,
                eventCategory=0,
                eventType=typeEventLog,
                strings=[message],
                data=b''
            )
        except Exception as e:
            raise ValueError(e)
        


