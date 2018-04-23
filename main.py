import time
from random import randint
from sense_hat import SenseHat

sense = SenseHat()
sense.clear(0, 0, 0)

bmap = [[],[]]
block = []
gameover = False

#Configuration
ttf = 1 # Time-to-fall, in seconds, time for a block to fall one level

def gen_tetromino() :
    # 0 = O-block XX
    #             XX
    #
    # 1 = I-block XXXX
    #
    # 2 = Z-block XX
    #              XX
    #
    # 3 = S-block  XX
    #             XX
    #
    # 4 = T-block  X
    #             XXX
    #
    # 5 = J-block X
    #             XXX
    #
    # 6 = L-block   X
    #             XXX
    #
    # Block = [[x0,y0],[x1,y1],[x2,y2],[x3,y3],colour,type,rotation]
    global block
    blocktype = randint(0,6)
    # tl = Top-left reference
    if(blocktype == 0):
        tl = randint(0,6)
        block = [[tl,-2],[tl+1,-2],[tl,-1],[tl+1,-1], [255,255,0], 0, 0]
    elif(blocktype == 1):
        tl = randint(0,4)
        block = [[tl,-1],[tl+1,-1],[tl+2,-1],[tl+3,-1], [0,255,255], 1, 0]
    elif(blocktype == 2):
        tl = randint(0,5)
        block = [[tl,-2],[tl+1,-2],[tl+1,-1],[tl+2,-1], [255,0,0], 2, 0]
    elif(blocktype == 3):
        tl = randint(0,5)
        block = [[tl,-1],[tl+1,-1],[tl+1,-2],[tl+2,-2], [0,255,0], 3, 0]
    elif(blocktype == 4):
        tl = randint(0,5)
        block = [[tl+1,-2],[tl,-1],[tl+1,-1],[tl+2,-1], [238,130,238], 4, 0]
    elif(blocktype == 5):
        tl = randint(0,5)
        block = [[tl,-2],[tl,-1],[tl+1,-1],[tl+2,-1], [0,0,255], 5, 0]
    elif(blocktype == 6):
        tl = randint(0,5)
        block = [[tl+2,-2],[tl,-1],[tl+1,-1],[tl+2,-1], [255,165,0], 6, 0]

def falling():
    global bmap
    global block
    global gameover
    # If any piece of block does not touch map or floor go down
    if (not hits_something()):
        for i in range(0,4):
            block[i][1] = block[i][1] + 1
    else:
        # If collision happens, first check if game is not over, else add every piece of block to the block map
        for i in range(0,4):
            if block[i][1] < 0:
                gameover = True
        for i in range (0,4):
            bmap[0].append(block[i])
            bmap[1].append(block[4])
        # Overwrites current active tetromino by generating a new one
        gen_tetromino()
    return True

def erase_lines(bmap, polte, floors):
    for l in range(0,len(polte)):
        for b in range(0,8):
            sense.set_pixel(bmap[0][polte[l][b]][0], bmap[0][polte[l][b]][1], 255, 255, 255)
            bmap[0][polte[l][b]] = [-1, -1]
            bmap[0][polte[l][b]] = [-1, -1]
    time.sleep(0.5)
    i = len(bmap[0]) - 1
    while i >= 0:
        if bmap[0][i] == [-1, -1]:
            del bmap[0][i]
            del bmap[1][i]
        i -= 1
    # Let gravity accomodate bmap
    for f in range(8, -1, -1):
        if f in floors:
            for b in range(0, len(bmap[0])):
                if bmap[0][b][1] < f:
                    bmap[0][b][1] += 1

def check_lines():
    global bmap
    global block
    fl0 = []
    fl1 = []
    fl2 = []
    fl3 = []
    fl4 = []
    fl5 = []
    fl6 = []
    fl7 = []
    floors = []
    # position of lines to Erase
    polte = []
    if len(bmap[0]) > 0:
        for i in range(0,len(bmap[0])):
            # Check every floor (y position)
            if bmap[0][i][1] == 7:
                fl7.append(i)
            elif bmap[0][i][1] == 6:
                fl6.append(i)
            elif bmap[0][i][1] == 5:
                fl5.append(i)
            elif bmap[0][i][1] == 4:
                fl4.append(i)
            elif bmap[0][i][1] == 3:
                fl3.append(i)
            elif bmap[0][i][1] == 2:
                fl2.append(i)
            elif bmap[0][i][1] == 1:
                fl1.append(i)
            elif bmap[0][i][1] == 0:
                fl0.append(i)
        if len(fl7) == 8:
            polte.append(fl7)
            floors.append(7)
        if len(fl6) == 8:
            polte.append(fl6)
            floors.append(6)
        if len(fl5) == 8:
            polte.append(fl5)
            floors.append(5)
        if len(fl4) == 8:
            polte.append(fl4)
            floors.append(4)
        if len(fl3) == 8:
            polte.append(fl3)
            floors.append(3)
        if len(fl2) == 8:
            polte.append(fl2)
            floors.append(2)
        if len(fl1) == 8:
            polte.append(fl1)
            floors.append(1)
        if len(fl0) == 8:
            polte.append(fl0)
            floors.append(0)
        if polte != []:
            erase_lines(bmap, polte, floors)

def draw_map():
    global bmap
    global block

    for i in range(0,4):
        if((block[i][1]>=0) and (block[i][1]<=7)):
            sense.set_pixel(block[i][0], block[i][1], block[4][0], block[4][1], block[4][2])
    for i in range(0,len(bmap[0])):
        sense.set_pixel(bmap[0][i][0], bmap[0][i][1], bmap[1][i][0], bmap[1][i][1], bmap[1][i][2])

def hits_something():
    global bmap
    global block

    hits = False
    for i in range(0,4):
        # If a falling piece of block matches another or touches floor
        if ([block[i][0],block[i][1] +1] in bmap[0]) or (block[i][1] + 1 == 8):
            hits = True
    return hits
        
# Complete unmaintanable hard-coded rotation function
def rotate(event):
    global block
    global bmap
    
    if event.action == 'pressed':
        if block[5] == 1 and block[6] == 0:
            if ([block[0][0], block[0][1] - 1] not in bmap[0] and 
            [block[0][0], block[0][1] - 2] not in bmap[0] and
            [block[0][0] + 1, block[0][1] - 1] not in bmap[0] and
            [block[0][0] + 1, block[0][1] - 2] not in bmap[0] and
            [block[0][0] + 1, block[0][1] - 3] not in bmap[0] and
            [block[0][0] + 2, block[0][1] - 1] not in bmap[0] and
            [block[0][0] + 2, block[0][1] - 2] not in bmap[0] and
            [block[0][0] + 2, block[0][1] - 3] not in bmap[0] and
            [block[0][0] + 3, block[0][1] - 1] not in bmap[0] and
            [block[0][0] + 3, block[0][1] - 2] not in bmap[0] and
            [block[0][0] + 3, block[0][1] - 3] not in bmap[0]):
                block[0] = [block[0][0] + 3, block[0][1] - 3]
                block[1] = [block[1][0] + 2, block[1][1] - 2]
                block[2] = [block[2][0] + 1, block[2][1] - 1]
                block[3] = [block[3][0] , block[3][1]]
                block[6] = 90
        elif block[5] == 1 and block[6] == 90:
            if (block[0][0] > 2 and
            [block[0][0] - 3, block[0][1]] not in bmap[0] and 
            [block[0][0] - 2, block[0][1]] not in bmap[0] and
            [block[0][0] - 1, block[0][1]] not in bmap[0] and
            [block[0][0] - 3, block[0][1] + 1] not in bmap[0] and
            [block[0][0] - 2, block[0][1] + 1] not in bmap[0] and
            [block[0][0] - 1, block[0][1] + 1] not in bmap[0] and
            [block[0][0] - 3, block[0][1] + 2] not in bmap[0] and
            [block[0][0] - 2, block[0][1] + 2] not in bmap[0] and
            [block[0][0] - 1, block[0][1] + 2] not in bmap[0] and
            [block[0][0] - 3, block[0][1] + 3] not in bmap[0] and
            [block[0][0] - 2, block[0][1] + 3] not in bmap[0] and
            [block[0][0] - 1, block[0][1] + 3] not in bmap[0]):
                block[0] = [block[0][0] - 3, block[0][1] + 3]
                block[1] = [block[1][0] - 2, block[1][1] + 2]
                block[2] = [block[2][0] - 1, block[2][1] + 1]
                block[3] = [block[3][0] , block[3][1]]
                block[6] = 0
        elif block[5] == 2 and block[6] == 0:
            if ([block[0][0] , block[0][1] + 1] not in bmap[0] and
            [block[0][0] , block[0][1] - 1] not in bmap[0] and
            [block[0][0] + 1, block[0][1] - 1] not in bmap[0] and
            [block[0][0] + 2, block[0][1] - 1] not in bmap[0] and
            [block[0][0] + 2, block[0][1]] not in bmap[0]):
                block[0] = [block[0][0] + 2, block[0][1] -1]
                block[1] = [block[1][0] + 1, block[1][1]]
                block[2] = [block[2][0], block[2][1] -1]
                block[3] = [block[3][0] - 1, block[3][1]]
                block[6] = 90
        elif block[5] == 2 and block[6] == 90:
            if (block[0][0] > 1 and
            [block[0][0] - 2, block[0][1]] not in bmap[0] and
            [block[0][0] - 1, block[0][1]] not in bmap[0] and
            [block[0][0] - 2, block[0][1] + 1] not in bmap[0] and
            [block[0][0] - 2, block[0][1] + 2] not in bmap[0] and
            [block[0][0], block[0][1] + 2] not in bmap[0]):
                block[0] = [block[0][0] - 2, block[0][1] + 1]
                block[1] = [block[1][0] - 1, block[1][1]]
                block[2] = [block[2][0], block[2][1] + 1]
                block[3] = [block[3][0] + 1, block[3][1]]
                block[6] = 0
        elif block[5] == 3 and block[6] == 0:
            if ([block[0][0] , block[0][1] - 1] not in bmap[0] and
            [block[0][0], block[0][1] - 2] not in bmap[0] and
            [block[0][0] + 1, block[0][1] - 2] not in bmap[0] and
            [block[0][0] + 2, block[0][1] - 2] not in bmap[0] and
            [block[0][0] + 2, block[0][1]] not in bmap[0]):
                block[0] = [block[0][0], block[0][1] - 2]
                block[1] = [block[1][0] - 1, block[1][1] - 1]
                block[2] = [block[2][0], block[2][1]]
                block[3] = [block[3][0] - 1, block[3][1] + 1]
                block[6] = 90
        elif block[5] == 3 and block[6] == 90:
            if (block[0][0] < 6 and
            [block[0][0] + 1, block[0][1]] not in bmap[0] and
            [block[0][0] + 2, block[0][1]] not in bmap[0] and
            [block[0][0] + 2, block[0][1] + 1] not in bmap[0] and
            [block[0][0] + 2, block[0][1] + 2] not in bmap[0] and
            [block[0][0], block[0][1] + 2] not in bmap[0]):
                block[0] = [block[0][0], block[0][1] + 2]
                block[1] = [block[1][0] + 1, block[1][1] + 1]
                block[2] = [block[2][0], block[2][1]]
                block[3] = [block[3][0] + 1, block[3][1] - 1]
                block[6] = 0
        elif block[5] == 4 and block[6] == 0:
            if ([block[0][0] - 1, block[0][1] - 1] not in bmap[0] and
            [block[0][0] - 1, block[0][1]] not in bmap[0]):
                block[0] = [block[0][0], block[0][1]]
                block[1] = [block[1][0], block[1][1] - 2]
                block[2] = [block[2][0] - 1, block[2][1] - 1]
                block[3] = [block[3][0] - 2, block[3][1]]
                block[6] = 90
        elif block[5] == 4 and block[6] == 90:
            if (block[0][0] < 7 and
            [block[0][0], block[0][1] - 1] not in bmap[0] and
            [block[0][0] + 1, block[0][1] - 1] not in bmap[0]):
                block[0] = [block[0][0], block[0][1]]
                block[1] = [block[1][0] + 2, block[1][1]]
                block[2] = [block[2][0] + 1, block[2][1] - 1]
                block[3] = [block[3][0], block[3][1] - 2]
                block[6] = 180
        elif block[5] == 4 and block[6] == 180:
            if ([block[0][0] + 1, block[0][1]] not in bmap[0] and
            [block[0][0] + 1, block[0][1] + 1] not in bmap[0]):
                block[0] = [block[0][0], block[0][1]]
                block[1] = [block[1][0], block[1][1] + 2]
                block[2] = [block[2][0] + 1, block[2][1] + 1]
                block[3] = [block[3][0] + 2, block[3][1]]
                block[6] = 270
        elif block[5] == 4 and block[6] == 270:
            if (block[0][0] > 0 and
            [block[0][0], block[0][1] + 1] not in bmap[0] and
            [block[0][0] - 1, block[0][1] + 1] not in bmap[0]):
                block[0] = [block[0][0], block[0][1]]
                block[1] = [block[1][0] - 2, block[1][1]]
                block[2] = [block[2][0] - 1, block[2][1] + 1]
                block[3] = [block[3][0], block[3][1] + 2]
                block[6] = 0
        elif block[5] == 5 and block[6] == 0:
            if ([block[0][0] + 1, block[0][1]] not in bmap[0] and
            [block[0][0] + 2, block[0][1]] not in bmap[0] and
            [block[0][0] + 1, block[0][1] + 2] not in bmap[0]):
                block[0] = [block[0][0] + 2, block[0][1]]
                block[1] = [block[1][0] + 1, block[1][1] - 1]
                block[2] = [block[2][0], block[2][1]]
                block[3] = [block[3][0] - 1, block[3][1] + 1]
                block[6] = 90
        elif block[5] == 5 and block[6] == 90:
            if (block[0][0] > 1 and
            [block[0][0], block[0][1] + 1] not in bmap[0] and
            [block[0][0], block[0][1] + 2] not in bmap[0] and
            [block[0][0] - 2, block[0][1] + 1] not in bmap[0]):
                block[0] = [block[0][0], block[0][1] + 2]
                block[1] = [block[1][0] + 1, block[1][1] + 1]
                block[2] = [block[2][0], block[2][1]]
                block[3] = [block[3][0] - 1, block[3][1] - 1]
                block[6] = 180
        elif block[5] == 5 and block[6] == 180:
            if ([block[0][0] - 1, block[0][1]] not in bmap[0] and
            [block[0][0] - 2, block[0][1]] not in bmap[0] and
            [block[0][0] - 1, block[0][1] - 2] not in bmap[0]):
                block[0] = [block[0][0] - 2, block[0][1]]
                block[1] = [block[1][0] - 1, block[1][1] + 1]
                block[2] = [block[2][0], block[2][1]]
                block[3] = [block[3][0] + 1, block[3][1] - 1]
                block[6] = 270
        elif block[5] == 5 and block[6] == 270:
            if (block[0][0] < 6 and
            [block[0][0], block[0][1] - 1] not in bmap[0] and
            [block[0][0], block[0][1] - 2] not in bmap[0] and
            [block[0][0] + 2, block[0][1] - 1] not in bmap[0]):
                block[0] = [block[0][0], block[0][1] - 2]
                block[1] = [block[1][0] - 1, block[1][1] - 1]
                block[2] = [block[2][0], block[2][1]]
                block[3] = [block[3][0] + 1, block[3][1] + 1]
                block[6] = 0
        elif block[5] == 6 and block[6] == 0:
            if ([block[0][0] - 1, block[0][1]] not in bmap[0] and
            [block[0][0], block[0][1] + 2] not in bmap[0] and
            [block[0][0] - 1, block[0][1] + 2] not in bmap[0]):
                block[0] = [block[0][0], block[0][1] + 2]
                block[1] = [block[1][0] + 1, block[1][1] - 1]
                block[2] = [block[2][0], block[2][1]]
                block[3] = [block[3][0] - 1, block[3][1] + 1]
                block[6] = 90
        elif block[5] == 6 and block[6] == 90:
            if (block[0][0] > 1 and
            [block[0][0], block[0][1] - 1] not in bmap[0] and
            [block[0][0] - 2, block[0][1]] not in bmap[0] and
            [block[0][0] - 2, block[0][1] - 1] not in bmap[0]):
                block[0] = [block[0][0] - 2, block[0][1]]
                block[1] = [block[1][0] + 1, block[1][1] + 1]
                block[2] = [block[2][0], block[2][1]]
                block[3] = [block[3][0] - 1, block[3][1] - 1]
                block[6] = 180
        elif block[5] == 6 and block[6] == 180:
            if ([block[0][0] + 1, block[0][1]] not in bmap[0] and
            [block[0][0], block[0][1] - 2] not in bmap[0] and
            [block[0][0] + 1, block[0][1] - 2] not in bmap[0]):
                block[0] = [block[0][0], block[0][1] - 2]
                block[1] = [block[1][0] - 1, block[1][1] + 1]
                block[2] = [block[2][0], block[2][1]]
                block[3] = [block[3][0] + 1, block[3][1] - 1]
                block[6] = 270
        elif block[5] == 6 and block[6] == 270:
            if (block[0][0] < 6 and
            [block[0][0], block[0][1] + 1] not in bmap[0] and
            [block[0][0] + 2, block[0][1]] not in bmap[0] and
            [block[0][0] + 2, block[0][1] + 1] not in bmap[0]):
                block[0] = [block[0][0] + 2, block[0][1]]
                block[1] = [block[1][0] - 1, block[1][1] - 1]
                block[2] = [block[2][0], block[2][1]]
                block[3] = [block[3][0] + 1, block[3][1] + 1]
                block[6] = 0

def move_left(event):
    global block
    if event.action=='pressed' and block[0][0] > 0 and block[1][0] > 0 and block[2][0] > 0 and block[3][0] > 0 and ([block[0][0] - 1, block[0][1]] not in bmap[0]) and ([block[1][0] - 1, block[1][1]] not in bmap[0]) and ([block[2][0] - 1, block[2][1]] not in bmap[0]) and ([block[3][0] - 1, block[3][1]] not in bmap[0]):
        for i in range(0,4):
            block[i][0] = block[i][0] - 1

def move_right(event):
    global block
    if event.action=='pressed' and block[3][0] < 7 and block[2][0] < 7 and block[1][0] < 7 and block[0][0] < 7 and ([block[0][0] + 1, block[0][1]] not in bmap[0]) and ([block[1][0] + 1, block[1][1]] not in bmap[0]) and ([block[2][0] + 1, block[2][1]] not in bmap[0]) and ([block[3][0] + 1, block[3][1]] not in bmap[0]):
        for i in range(0,4):
            block[i][0] = block[i][0] + 1

sense.stick.direction_left = move_left
sense.stick.direction_right = move_right
sense.stick.direction_up = rotate

gen_tetromino()
start_time = time.time()
while (not gameover):
    elapsed_time = time.time() - start_time
    if elapsed_time > ttf:
        falling()
        check_lines()
        start_time = time.time()
    if (not gameover):
        draw_map()
    time.sleep(0.1)
    sense.clear(0, 0, 0)
sense.show_message("Game Over")
