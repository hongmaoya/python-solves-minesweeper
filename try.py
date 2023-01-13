import pyautogui as pya
import time
import keyboard

NX, NY = 16, 30  # number of rows and columns
N = NX * NY  # number of cell
UPPER, LOWER, LEFT, RIGHT = 5, 4, 5, 4  # useless Pixel
CELLX, CELLY = 24, 24  # Length and width of each cell
OFFSET = 10  # a offset of the coordinates
MINE, FLAG, INITIAL = 9, 10, 11


# numbering start from one
def GetId(x, y):
    return (x - 1) * NY + y
# x-axis direction: top to bottom
# y-axis direction: left to right


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
        if res != None:
            pya.leftClick(res[0] + OFFSET, res[1] + OFFSET)
        location = pya.locateOnScreen(difficulty_fig)
    print('{:.^30}'.format('\'location\' ready'))
    global left, top, Szx, Szy
    left, top, Szy, Szx = location[0], location[1], location[2], location[3]


def Init():
    global cell, status, judgment, cellx, celly
    cell = [[0, 0] for i in range(N + 1)]
    # cell stores the coordinates of the upper left corner of all cells
    status = [10 for i in range(N + 1)]
    # i-th cell have been clicked
    # 0~8: number 0 to 8 ,9: flag, 10: initial
    judgment = [10 for i in range(N + 1)]
    # we can kown what is i-th cell
    # 10: unkown, 9: mine
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
    cellx, celly = [0], [0]
    for i in range(1, NX + 1):
        cellx.append(cell[GetId(i, 1)][1])
    for i in range(1, NY + 1):
        celly.append(cell[GetId(1, i)][0])
    print('{:.^30}'.format('\'cell\' ready'))


def IsDead():
    dead = pya.locateOnScreen('./Arbiter/die.png')
    if dead == None:
        return False
    return True


def ClickLeft(id):
    pya.leftClick(cell[id][0] + OFFSET, cell[id][1] + OFFSET, _pause=False)
    if IsDead():
        print('{:.^30}'.format('!!DIE!!'))
        main()


def ClickRight(id):
    pya.rightClick(cell[id][0] + OFFSET, cell[id][1] + OFFSET, _pause=False)
    status[id] = judgment[id] = MINE


def ClickMid():
    pya.middleClick(cell[id][0] + OFFSET, cell[id][1] + OFFSET, _pause=False)


def Restart():
    print('{:.^30}'.format('restarting'))
    time.sleep(1)
    dead = pya.locateOnScreen('./Arbiter/die.png')
    pya.leftClick(dead[0] + OFFSET, dead[1] + OFFSET)


# biggest number that smaller than or equal to x
def lower_bound(a, x):
    l, r, ans = 1, len(a) - 1, -1
    while r >= l:
        mid = (l + r) // 2
        if (a[mid] <= x):
            l = mid + 1
            ans = mid
        else:
            r = mid - 1
    return ans


def LocationCell(lef, op):
    return lower_bound(cellx, op), lower_bound(celly, lef)


def Now():
    print('{:.^30}'.format('\'Now\' ready'))
    pass


def Solve():
    pass


def test():
    global cellx, celly
    cellx = [0, 526, 550, 574, 598, 622, 646, 670, 694, 718, 742, 766, 790, 814, 838, 862, 886]
    celly = [0, 1808, 1832, 1856, 1880, 1904, 1928, 1952, 1976, 2000, 2024, 2048, 2072, 2096, 2120, 2144, 2168, 2192, 2216, 2240, 2264, 2288, 2312, 2336, 2360, 2384, 2408, 2432, 2456, 2480, 2504]
    print('in test')
    # time.sleep(2)
    # print('end sleep')
    test = pya.locateAllOnScreen('./Arbiter/9.png', confidence=0.99)
    cnt = 0
    for i in test:
        cnt += 1
        print(i[0],i[1])
        print(LocationCell(i[0], i[1]))
    print(cnt)
    pass


def main():
    # if IsDead():
    #     Restart()
    # GetLocation()
    # Init()
    test()
    # Now()
    # Solve()
    pass


if __name__ == '__main__':
    time.sleep(0.5)
    main()
