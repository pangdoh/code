import win32api
import win32con
win32api.keybd_event(17, 0, 0, 0)  #ctrl键位码是17
win32api.keybd_event(86, 0, 0, 0)  #v键位码是86
win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0) #释放按键
win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
