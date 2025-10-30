from Helpers.GettingSettings import GettingSettings
from Helpers.SeleniumHelper import SeleniumHelper
import win32api
import win32con
import win32gui
import win32ts
import time

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


    def _wndproc(self, hwnd, msg, wparam, lparam):
        if msg == self.WM_WTSESSION_CHANGE:
            event = wparam
            sessionID = lparam

            if event == self.WTS_SESSION_UNLOCK:
                userLogin = self._getSessionUser(sessionID)

                if userLogin and userLogin == self._userPC:
                    #Log this event in the windows logger
                    self._inSeleniumHelper.execProcess()
                    print(f"INICIANDO SESIÓN CON: {userLogin}")

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
            time.sleep(0.1)
