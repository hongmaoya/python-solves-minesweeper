import pyautogui
import time

# numbering start from one
NX, NY = 16, 30
N = NX * NY
UPPER, LOWER, LEFT, RIGHT = 5, 4, 5, 4
CELLX, CELLY = 24, 24


def GetId(x, y):
    return (x - 1) * NY + y


def GetXY(id):
    return (id - 1) // NY + 1, (id - 1) % NY + 1


def main():
    # difficulty = pyautogui.confirm('select the difficulty', buttons=['Beginner', 'Intermediate', 'Expert'])
    difficulty = 'Expert'
    difficulty_fig = './Arbiter/difficulty/' + difficulty + '.png'
    location = pyautogui.locateOnScreen(difficulty_fig)
    print('{:.^30}'.format('Finding'))
    while location == None:
        location = pyautogui.locateOnScreen(difficulty_fig)
    print('{:.^30}'.format('\'location\' ready'))
    print(location)
    global left, top
    left, top = location[0], location[1]
    cell = [[0, 0] for i in range(N + 1)]
    # x-axis direction:top to bottom
    # y-axis direction:left to right
    # cell stores the coordinates of the upper left corner of all cells
    for i in range(1, N + 1):
        x, y = GetXY(i)
        print(i, x, y)
        if (x == 1):
            cell[i][1] = top + UPPER
            if(y == 1):
                cell[i][0] = left + LEFT
            else:
                cell[i][0] = cell[i - 1][0] + CELLY
        else:
            cell[i][1] = cell[i - NY][1] + CELLX
            if(y == 1):
                cell[i][0] = left + LEFT
            else:
                cell[i][0] = cell[i - 1][0] + CELLY
        pyautogui.click(cell[i][0], cell[i][1], button='right')


if __name__ == '__main__':
    # time.sleep(0.5)
    main()
