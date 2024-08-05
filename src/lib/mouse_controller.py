import time
import pyautogui


def get_current_position():
    for i in range(3):
        print(str(i))
        time.sleep(1)
    xy = pyautogui.position()
    print(xy.x)
    print(xy.y)


def move_to_point(x,y):
    pyautogui.moveTo(x, y, 0.1)


def click_left_button():
    pyautogui.click()


