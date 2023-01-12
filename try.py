import pyautogui as pya
import time
import keyboard

# numbering start from one
NX, NY = 16, 30
N = NX * NY
UPPER, LOWER, LEFT, RIGHT = 5, 4, 5, 4
CELLX, CELLY = 24, 24
OFFSET = 10
MINE, FLAG, INITIAL = 9, 10, 11


def GetId(x, y):
    return (x - 1) * NY + y
# x-axis direction:top to bottom
# y-axis direction:left to right


def GetXY(id):
    return (id - 1) // NY + 1, (id - 1) % NY + 1


def GetLocation():
    # difficulty = pya.confirm('select the difficulty', buttons=['Beginner', 'Intermediate', 'Expert'])
    difficulty = 'Expert'
    difficulty_fig = './Arbiter/difficulty/' + difficulty + '.png'
    location = pya.locateOnScreen(difficulty_fig)
    print('{:.^30}'.format('Finding'))
    while location == None:
        res = pya.locateOnScreen('./Arbiter/nodie.png')
        pya.leftClick(res[0] + OFFSET, res[1] + OFFSET)
        location = pya.locateOnScreen(difficulty_fig)
    print('{:.^30}'.format('\'location\' ready'))
    print(location)
    global left, top, Szx, Szy
    left, top, Szy, Szx = location[0], location[1], location[2], location[3]


def Init():
    global cell, status, judgment
    cell = [[0, 0] for i in range(N + 1)]
    # cell stores the coordinates of the upper left corner of all cells
    status = [11 for i in range(N + 1)]
    # i-th cell have been clicked
    # 0~8: number 0 to 8 ,9: flag, 10: initial
    judgment = [11 for i in range(N + 1)]
    # we can kown what is i-th cell
    for i in range(1, N + 1):
        x, y = GetXY(i)
        if (x == 1):
            cell[i][1] = top + UPPER
            if (y == 1):
                cell[i][0] = left + LEFT
            else:
                cell[i][0] = cell[i - 1][0] + CELLY
        else:
            cell[i][1] = cell[i - NY][1] + CELLX
            if (y == 1):
                cell[i][0] = left + LEFT
            else:
                cell[i][0] = cell[i - 1][0] + CELLY
        ClickLeft(i)
    print('{:.^30}'.format('\'cell\' ready'))


def isdead():
    dead = pya.locateOnScreen('./Arbiter/die.png')
    if dead == None:
        return False
    return True


def ClickLeft(id):
    pya.leftClick(cell[id][0] + OFFSET, cell[id][1] + OFFSET, _pause=False)
    if isdead():
        print('{:.^30}'.format('!!DIE!!'))
        main()


def ClickRight(id):
    pya.rightClick(cell[id][0] + OFFSET, cell[id][1] + OFFSET, _pause=False)
    status[id] = judgment[id] = MINE


def ClickMid():
    pya.middleClick(cell[id][0] + OFFSET, cell[id][1] + OFFSET, _pause=False)


def restart():
    print('{:.^30}'.format('restarting'))
    time.sleep(1)
    dead = pya.locateOnScreen('./Arbiter/die.png')
    pya.leftClick(dead[0] + OFFSET, dead[1] + OFFSET)


def main():
    if isdead():
        restart()
    GetLocation()
    Init()


if __name__ == '__main__':
    time.sleep(0.5)
    main()
