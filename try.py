import pyautogui as pya
import time
import keyboard

NX, NY = 16, 30  # number of rows and columns
N = NX * NY  # number of cell
UPPER, LOWER, LEFT, RIGHT = 5, 4, 5, 4  # useless Pixel
CELLX, CELLY = 24, 24  # Length and width of each cell
OFFSET = 10  # a offset of the coordinates
MINE, FLAG, INITIAL = 9, 10, 11


def GetLocation():
    # difficulty = pya.confirm('select the difficulty', buttons=['Beginner', 'Intermediate', 'Expert'])
    difficulty = 'Expert'
    difficulty_path = './Arbiter/difficulty/' + difficulty + '.png'
    location = pya.locateOnScreen(difficulty_path)
    print('{:.^30}'.format('Finding'))
    while location == None:
        res = pya.locateOnScreen('./Arbiter/nodie.png')
        if res != None:
            pya.leftClick(res[0] + OFFSET, res[1] + OFFSET)
        location = pya.locateOnScreen(difficulty_path)
    print('{:.^30}'.format('\'location\' ready'))
    global left, top, Szx, Szy
    left, top, Szy, Szx = location[0], location[1], location[2], location[3]


# cellx, celly = [0], [0]
cellx = [0, 461, 485, 509, 533, 557, 581, 605,
         629, 653, 677, 701, 725, 749, 773, 797, 821]
celly = [0, 1810, 1834, 1858, 1882, 1906, 1930, 1954, 1978, 2002, 2026, 2050, 2074, 2098, 2122,
         2146, 2170, 2194, 2218, 2242, 2266, 2290, 2314, 2338, 2362, 2386, 2410, 2434, 2458, 2482, 2506]
cell = [[0, 0] for i in range(N + 1)]
# cell stores the coordinates of the upper left corner of all cells
status = [10 for i in range(N + 1)]
# i-th cell have been clicked
# 0~8: number 0 to 8 ,9: flag, 10: initial
judgment = [10 for i in range(N + 1)]
# we can kown what is i-th cell
# 10: unkown, 9: mine


def Init():
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
    for i in range(1, NX + 1):
        cellx.append(cell[GetId(i, 1)][1])
    for i in range(1, NY + 1):
        celly.append(cell[GetId(1, i)][0])
    print('{:.^30}'.format('\'cell\' ready'))

# numbering start from one


def GetId(x, y):
    return (x - 1) * NY + y
# x-axis direction: top to bottom
# y-axis direction: left to right


def GetXY(id):
    return (id - 1) // NY + 1, (id - 1) % NY + 1


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
    for i in range(1, 10):
        path = './Arbiter/' + str(i) + '.png'
        position = pya.locateAllOnScreen(path, confidence=0.99, region = (left, top, Szy, Szx))
        for posi in position:
            a, b = LocationCell(posi[0], posi[1])
            status[GetId(a, b)] = i
    print('{:.^30}'.format('\'Now\' ready'))


def Solve():
    pass


def test():
    for i in range(1, NX + 1):
        for j in range(1, NY + 1):
            print('{:^2}'.format(status[GetId(i, j)]), end=' ')
        print()
    pass


def main():
    # if IsDead():
    #     Restart()
    # GetLocation()
    # Init()
    global left, top, Szy, Szx 
    left, top, Szy, Szx = 1805, 456, 729, 393
    Now()
    test()
    # Solve()
    pass


if __name__ == '__main__':
    time.sleep(0.5)
    main()
