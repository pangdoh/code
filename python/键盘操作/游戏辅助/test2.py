from ctypes import *
import PyHook3
import pythoncom


def onKeyboardEvent(event):
    print('='*30)
    # event.WindowName有时候会不好用
    # 所以调用底层API喊来获取窗口标题
    windowTitle = create_string_buffer(512)
    windll.user32.GetWindowTextA(event.Window,byref(windowTitle),512)
    windowName = windowTitle.value.decode('gbk')
    print('当前您正处于"{0}"窗口'.format(windowName))
    print('刚刚按下了"{0}"键'.format(chr(event.Ascii)))
    return True


hm = PyHook3.HookManager()

hm.KeyDown = onKeyboardEvent
hm.HookKeyboard()

pythoncom.PumpMessages()
