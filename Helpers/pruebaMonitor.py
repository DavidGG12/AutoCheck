# monitor_desbloqueo.py
import time
from datetime import datetime

try:
    import win32api
    import win32con
    import win32gui
    import win32ts
except ImportError:
    raise SystemExit("Necesitas instalar pywin32: pip install pywin32")

# Constantes (asegurar valores correctos)
WM_WTSSESSION_CHANGE = 0x02B1
WTS_SESSION_LOCK = 0x7       # sesión bloqueada
WTS_SESSION_UNLOCK = 0x8     # sesión desbloqueada

# Fallback para el modo de notificación (algunas versiones exponen estas constantes)
NOTIFY_FOR_THIS_SESSION = getattr(win32ts, "NOTIFY_FOR_THIS_SESSION", 0)
NOTIFY_FOR_ALL_SESSIONS = getattr(win32ts, "NOTIFY_FOR_ALL_SESSIONS", 1)

LOG_FILE = "desbloqueos.log"

def get_session_user(session_id):
    """
    Devuelve "DOMAIN\\User" o None si no se puede obtener.
    """
    try:
        user_raw = win32ts.WTSQuerySessionInformation(None, session_id, win32ts.WTSUserName)
        domain_raw = win32ts.WTSQuerySessionInformation(None, session_id, win32ts.WTSDomainName)

        # Normalizar distintos tipos de retorno
        user = user_raw[0] if isinstance(user_raw, (list, tuple)) and user_raw else user_raw
        domain = domain_raw[0] if isinstance(domain_raw, (list, tuple)) and domain_raw else domain_raw

        # Si vienen como bytes, decode
        if isinstance(user, bytes):
            user = user.decode(errors="ignore")
        if isinstance(domain, bytes):
            domain = domain.decode(errors="ignore")

        if user:
            return f"{domain}\\{user}" if domain else user
        return None
    except Exception as ex:
        # Si algo falla devolvemos None (pero no rompemos el flujo)
        return None

def log_line(line: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full = f"{ts} - {line}"
    print(full)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(full + "\n")
    except Exception:
        # No romper si falla escribir el archivo; ya imprimimos en consola
        pass

def wndproc(hwnd, msg, wparam, lparam):
    # Recibe mensajes de la ventana; filtramos WM_WTSSESSION_CHANGE
    if msg == WM_WTSSESSION_CHANGE:
        event = wparam
        session_id = lparam  # lParam contiene el session id
        if event == WTS_SESSION_UNLOCK:
            user = get_session_user(session_id)
            if user:
                log_line(f"SESIÓN {session_id} DESBLOQUEADA por: {user}")
            else:
                log_line(f"SESIÓN {session_id} DESBLOQUEADA (usuario no disponible)")
        elif event == WTS_SESSION_LOCK:
            user = get_session_user(session_id)
            if user:
                log_line(f"SESIÓN {session_id} BLOQUEADA por: {user}")
            else:
                log_line(f"SESIÓN {session_id} BLOQUEADA (usuario no disponible)")

    # Devolver al procedimiento por defecto
    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

def main(monitor_all_sessions=False):
    # Registrar clase de ventana invisible
    wc = win32gui.WNDCLASS()
    hinst = wc.hInstance = win32api.GetModuleHandle(None)
    wc.lpszClassName = "SessionMonitorClass_Python"
    wc.lpfnWndProc = wndproc
    try:
        classAtom = win32gui.RegisterClass(wc)
    except Exception:
        # Si ya está registrada, continuar
        classAtom = None

    hwnd = win32gui.CreateWindowEx(
        0,
        wc.lpszClassName,
        "SessionMonitorHiddenWindow",
        0,
        0, 0, 0, 0,
        0, 0, hinst, None
    )

    # Registrar notificaciones de sesión
    notify_flag = NOTIFY_FOR_ALL_SESSIONS if monitor_all_sessions else NOTIFY_FOR_THIS_SESSION
    win32ts.WTSRegisterSessionNotification(hwnd, notify_flag)

    log_line("INICIADO: monitoreando bloqueos/desbloqueos de sesión")
    if monitor_all_sessions:
        log_line("Modo: NOTIFY_FOR_ALL_SESSIONS (requiere privilegios y puede monitorizar otras sesiones)")
    else:
        log_line("Modo: NOTIFY_FOR_THIS_SESSION (solo la sesión actual)")

    try:
        while True:
            # Procesar mensajes pendientes
            win32gui.PumpWaitingMessages()
            time.sleep(0.1)
    except KeyboardInterrupt:
        log_line("DETENIENDO: recibido Ctrl+C")
    finally:
        try:
            win32ts.WTSUnRegisterSessionNotification(hwnd)
            win32gui.DestroyWindow(hwnd)
        except Exception:
            pass

if __name__ == "__main__":
    # Si quieres intentar monitorear TODAS las sesiones, pon True (puede requerir elevación)
    main(monitor_all_sessions=False)
