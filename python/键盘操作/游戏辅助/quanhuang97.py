from pynput import keyboard
import win32api
import win32con
import time


# 按键按下监听
def on_press(key):
    try:
        print('press key {0}, vk: {1}'.format(key.char, key.vk))
        if "'h'" == str(key):
            print("技能1")
            # keyboard_ctrl.press('s')
            # keyboard.release('s')
            win32api.keybd_event(83, 0, 0, 0)  # s
            win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放s
            # time.sleep(0.1)
            # win32api.keybd_event(68, 0, 0, 0)  # d
            # win32api.keybd_event(68, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放d
            # time.sleep(0.1)
            # win32api.keybd_event(74, 0, 0, 0)  # j
            # win32api.keybd_event(74, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放j

    except AttributeError:
        print('special press key {0}, vk: {1}'.format(key, key.value.vk))


# 按键释放监听
def on_release(key):
    if key == keyboard.Key.esc:
        # 停止监听
        return False
    try:
        print('release key {0}, vk: {1}'.format(key.char, key.vk))
    except AttributeError:
        print('special release key {0}, vk: {1}'.format(key, key.value.vk))


# 键盘监听
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

