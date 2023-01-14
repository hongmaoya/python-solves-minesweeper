import pyautogui as pya
import time
import random
import keyboard

NX, NY = 16, 30  # number of rows and columns
N = NX * NY  # number of cell
UPPER, LOWER, LEFT, RIGHT = 5, 4, 5, 4  # useless pixel
CELLX, CELLY = 24, 24  # Length and width of each cell
OFFSET = 12  # a offset of the coordinates
FLAG, INITIAL = 9, 10
NUMBERMINES = 50


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
    # print(location)


def Init():
    global cellx, celly, cell, status, judgment
    cellx, celly = [0], [0]
    cell = [[0, 0] for i in range(N + 1)]
    # cell stores the coordinates of the upper left corner of all cells
    status = [10 for i in range(N + 1)]
    # i-th cell have been clicked
    # 0~8: number 0 to 8 ,9: flag, 10: initial
    judgment = [i for i in range(N + 1)]
    # if i in judgment then i isn't right clicked or middle clicked
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
    # print(cellx)
    # print(celly)

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
    # print(id, GetXY(id))
    # print(cell[id][0] + OFFSET, cell[id][1] + OFFSET)
    pya.leftClick(cell[id][0] + OFFSET, cell[id][1] + OFFSET, _pause=False)
    if IsDead():
        print('{:.^30}'.format('!!DIE!!'))
        main()


def ClickRight(id):
    global sign
    sign = 0
    pya.rightClick(cell[id][0] + OFFSET, cell[id][1] + OFFSET, _pause=False)
    status[id] = FLAG
    if id in judgment:
        judgment.remove(id)


def ClickMid(id):
    global sign
    sign = 0
    pya.middleClick(cell[id][0] + OFFSET, cell[id][1] + OFFSET, _pause=False)
    if id in judgment:
        judgment.remove(id)


def ClickRandom():
    while True:
        id = random.randint(1, len(judgment) - 1)
        if status[judgment[id]] == 10:
            ClickLeft(judgment[id])
            return


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


def Now_():
    t0 = time.time()
    pya.moveTo(10, 10)
    for i in range(1, 10):
        path = './Arbiter/' + str(i) + '.png'
        position = pya.locateAllOnScreen(
            path, confidence=0.99, region=(left, top, Szy, Szx))
        for posi in position:
            a, b = LocationCell(posi[0], posi[1])
            status[GetId(a, b)] = i
    loc = pya.screenshot()
    for i in range(1, N + 1):
        if status[i] == 10:
            if loc.getpixel((cell[i][0], cell[i][1]))[0] < 200:
                status[i] = 0
    print(time.time() - t0)
    # print('{:.^30}'.format('\'Now\' ready'))


def abs(x):
    return x if x >= 0 else -x


def Now():
    # t0 = time.time()
    loc = pya.screenshot()
    col = [
        [192, 192, 192], [0, 0, 255], [1, 128, 1], [255, 0, 0], [0, 0, 128],
        [128, 0, 0], [12, 132, 132], [0, 0, 0], [131, 131, 131]
    ]
    for i in range(1, N + 1):
        pix = loc.getpixel((cell[i][0] + OFFSET, cell[i][1] + OFFSET))
        for color, j in enumerate(col):
            if color == 0:
                continue
            flag = 1
            if color == 7:
                pix = loc.getpixel(
                    (cell[i][0] + OFFSET + 10, cell[i][1] + 10))

            for k in range(3):
                if abs(pix[k] - j[k]) > 1:
                    flag = 0
                    break
            if flag:
                status[i] = color
                break
        if status[i] == 10:
            if loc.getpixel((cell[i][0], cell[i][1]))[0] < 200:
                status[i] = 0
    # print(time.time() - t0)
    pass


def GetAround(id):
    if id not in judgment:
        return
    x, y = GetXY(id)
    Around = []
    for xx in range(x - 1, x + 1 + 1):
        for yy in range(y - 1, y + 1 + 1):
            if xx <= 0 or xx > NX or yy <= 0 or yy > NY or (xx == x and yy == y):
                continue
            if status[GetId(xx, yy)] > 8:
                Around.append(GetId(xx, yy))
    mines, blank = [], []
    for i in Around:
        if status[i] == 9:
            mines.append(i)
        else:
            blank.append(i)
    return Around, mines, blank


def Solve1():
    for i in range(1, N + 1):
        if status[i] == 0:
            if i in judgment:
                ClickMid(i)
        if status[i] < 9:
            if i in judgment:
                Around, mines, blank = GetAround(i)
                if Around == None:
                    continue
                # print(GetXY(i), status[i], mines, blank)
                mines, blank = len(mines), len(blank)
                if mines + blank == status[i]:
                    for j in Around:
                        if status[j] != FLAG:
                            ClickRight(j)
                if mines == status[i]:
                    if blank > 0:
                        ClickMid(i)
                    else:
                        judgment.remove(i)


def Getudlr(id):
    if id not in judgment:
        return
    x, y = GetXY(id)
    FX = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    udlr = []
    for fx, fy in FX:
        xx, yy = x + fx, y + fy
        if xx <= 0 or yy <= 0 or xx > NX or yy > NY:
            continue
        iid = GetId(x, y)
        if status[iid] > 0 and status[iid] < 9:
            udlr.append(iid)
    return udlr


def Solve2():
    for i in range(1, N + 1):
        if status[i] < 9:
            if i in judgment:
                minesi, blanksi = GetAround(i)[1::]
                if minesi == None:
                    continue
                if len(blanksi) > 0:
                    udlr = Getudlr(i)
                    if udlr == None:
                        continue
                    for j in udlr:
                        minesj, blanksj = GetAround(j)[1::]
                        if minesj == None:
                            continue
                        flag = 1
                        for elem in blanksi:
                            if elem not in blanksj:
                                flag = 0
                                break
                        if flag:
                            if status[j] - len(minesj) == status[i] - len(minesi):
                                for elem in blanksj:
                                    if elem not in blanksi:
                                        ClickLeft(elem)
                            elif (status[j] - len(minesj) - status[i] - len(minesi)) >= (len(blanksj) - len(blanksi)):
                                for elem in blanksj:
                                    if elem not in blanksi:
                                        ClickRight(elem)


# we can find that all the formalized series of moves(定式) can be launched by one or two cell
# So we first achieve the reasoning for both cases
def Solve():
    global sign
    sign = 1
    # Printf()
    Solve1()
    Solve2()
    if Cnt() == NUMBERMINES:
        for i in judgment[1:]:
            if status[i] == 10:
                print(i)
                ClickLeft(i)
        print('{:.^30}'.format('!!WIN!!'))
        exit()
    if sign:
        ClickRandom()


def Printf():
    for i in range(1, NX + 1):
        for j in range(1, NY + 1):
            print('{:^2}'.format(status[GetId(i, j)]), end=' ')
        print()
    print()


def Cnt():
    pya.moveTo(10, 10)
    ret = 0
    for num in status:
        if num == FLAG:
            ret += 1
    return ret


def main():
    if IsDead():
        Restart()
    GetLocation()
    Init()
    # for i in range(1, 16 + 1):
    #     for j in range(1, 30 + 1):
    #         print(cell[GetId(i, j)], end='')
    #     print()
    ClickRandom()
    while True:
        Now()
        Solve()
    # pass


if __name__ == '__main__':
    time.sleep(0.5)
    main()
