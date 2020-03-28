import win32api, win32gui, win32con

self = '约战竞技场-游戏(活跃)'


def show(self):
    # windows handlers
    # hwnd = self.window.handle
    hwnd = win32gui.FindWindow(self, None)
    win32gui.ShowWindow(hwnd, 1)

    win32gui.SetForegroundWindow(hwnd)
    # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE| win32con.SWP_NOOWNERZORDER|win32con.SWP_SHOWWINDOW)
    # X11LockScreenWindow.show(self)


show(self)  # 由于keybd_event需要激活才能成功发送快捷键
# send key
win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
win32api.keybd_event(115, 0, 0, 0)  # f4键位码是86
win32api.keybd_event(115, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
