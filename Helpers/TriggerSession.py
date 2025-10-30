from Helpers.GettingSettings import GettingSettings
from Helpers.SeleniumHelper import SeleniumHelper
from Helpers.InitDataBase import InitDataBase
from datetime import date, datetime, time
import time as tm
import win32api
import win32con
import win32gui
import win32ts

class TriggerSession:
    def __init__(self):
        self.WM_WTSESSION_CHANGE = 0x02B1
        self.WTS_SESSION_LOCK = 0x7
        self.WTS_SESSION_UNLOCK = 0x8
        self.NOTIFY_FOR_THIS_SESSION = getattr(win32ts, "NOTIFY_FOR_THIS_SESSION", 0)
        self.NOTIFY_FOR_ALL_SESSIONS = getattr(win32ts, "NOTIFY_FOR_ALL_SESSIONS", 1)

        self._inGettingSettings = GettingSettings()
        self._userPC = self._inGettingSettings.getSessionUser()

        self._inSeleniumHelper = SeleniumHelper()
        self._inDataBase = InitDataBase()
        
        try:
            self._inDataBase.creatingTable()
        except:
            pass

        #Definition of schedule that we need to execute proceess and actual time
        self._schedule = [time(8, 0), time(10, 0)]
        self._actualTime = datetime.now().time()

    def _getSessionUser(self, sessionId):
        try:
            userRaw = win32ts.WTSQuerySessionInformation(None, sessionId, win32ts.WTSUserName)
            userSession = userRaw[0] if isinstance(userRaw, (list, tuple)) and userRaw else userRaw

            if isinstance(userSession, bytes):
                userSession = userSession.decode(errors="ignore")
            if userSession:
                return userSession
            return None
        except Exception as ex:
            #Log this event in the windows logger
            return None

    def _validateSchedule(self):
        return True if(self._schedule[0] >= self._actualTime >= self._schedule[1]) else False 
    
    def _validateNumExecutions(self):
        return True if self._inDataBase.slExecuteProcess() == "0" else False

    def _wndproc(self, hwnd, msg, wparam, lparam):
        lol = self._validateNumExecutions()

        try:
            if msg == self.WM_WTSESSION_CHANGE and self._validateNumExecutions(): 
                event = wparam
                sessionID = lparam


                if event == self.WTS_SESSION_UNLOCK:
                    userLogin = self._getSessionUser(sessionID)

                    if userLogin and userLogin == self._userPC:
                        #Log this event in the windows logger
                        self._inSeleniumHelper.execProcess()
                        self._inDataBase.updExecuteProcess(newData="1")
                        print(f"INICIANDO SESIÓN CON: {userLogin}")
        except Exception as ex:
            self._inDataBase.updExecuteProcess(newData="0")

            #Put this error to the logger
            raise ValueError(ex)
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
    
    def execMonitor(self, monitorAllSessions=False):
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "SessionMonitorClass_Python"
        wc.lpfnWndProc = self._wndproc

        try:
            classAtom = win32gui.RegisterClass(wc)
        except Exception as ex:
            classAtom = None
        
        hwnd = win32gui.CreateWindowEx(
            0,
            wc.lpszClassName,
            "SessionMonitorHiddenWindow",
            0,
            0, 0, 0, 0,
            0, 0, hinst, None
        )

        notifyFlag = self.NOTIFY_FOR_ALL_SESSIONS if monitorAllSessions else self.NOTIFY_FOR_THIS_SESSION
        win32ts.WTSRegisterSessionNotification(hwnd, notifyFlag)

        while True:
            win32gui.PumpWaitingMessages()
            tm.sleep(0.1)

            if not self._validateSchedule() and self._actualTime >= self._schedule[1]:
                self._inDataBase.deletingTable()
                self._inDataBase.closeConnection()
