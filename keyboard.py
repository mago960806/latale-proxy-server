import winsound

from pynput import keyboard


def run_left():
    winsound.Beep(1000, 100)
    print("向左跑 3 秒")


def run_right():
    winsound.Beep(1200, 100)
    print("向右跑 3 秒")


with keyboard.GlobalHotKeys({"<ctrl>+1": run_left, "<ctrl>+2": run_right}) as hotkeys:
    hotkeys.join()
