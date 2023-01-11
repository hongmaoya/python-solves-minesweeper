import pyautogui
import time

# pyautogui.moveTo(1798, 848)


def main():
    # difficulty = pyautogui.confirm('select the difficulty', buttons=['Beginner', 'Intermediate', 'Expert'])
    difficulty = 'Expert'
    difficulty_fig = './Arbiter/difficulty/' + difficulty + '.png'
    location = pyautogui.locateOnScreen(difficulty_fig)
    print(location)
    init = pyautogui.locateAllOnScreen('./Arbiter/11.png')
    tot = 0
    for i in init:
        print(i)
        tot += 1
    print(tot)


if __name__ == '__main__':
    # time.sleep(0.5)
    main()
