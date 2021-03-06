#!/usr/bin/env python3
# -*- coding: utf-8 -*-
ABOUT = '''
# This file contains all the needed NE assembly functions:
#   DISPSTART   ($0: return_addr)
#   DISPWORD    ($0: return_addr)
#   DISPMENU    ($0: return_addr)
#   DISPCHAR    ($0: return_addr, $1: state)
#       state: 0: gg, 1: left1, 2: left2, 3: right1, 4: right2
#   CHECKVOLUME ($0: inst_addr if volume != 15, $1: inst_addr if volume == 15)
#   BLINK       (infinite loop, no input)
#   DISPMAP     ($0: return_addr, $1: centre_x, $2: centre_y)
#   GETMAPCOLOR ($3: x_coord, $4: y_coord, $5: return_addr)
#       return: ($6: color)
#   DISPENEMY   ($0: return_addr, $1: centre_x, $2: centre_y, $3: enemy_x_rel_map, $4: enemy_y_rel_map)
#   DIVISION    ($9: return_addr, $10: A, $11: B)
#       return: ($12: C)
#   MODULUS     ($9: return_addr, $10: A, $11: B)
#       return  ($12: C)
#   MULTIPLICATION ($12 = $10 * $11) ra $9
'''

CPU_FREQ = 100000000

def delayGenerator(sec, label):
    delcounter = int(sec * CPU_FREQ / 6)
    return "    LWi  $1, %d\n%s:\n    SUBi $1, $1, 1\n    BEQ  $1, 0\n    JUMP %s\n" % (delcounter, label, label)

OLEDX = 96
OLEDY = 64

# Load bitmaps (converted using convert.py):
images = {}
with open("../bitmaps/start.bitmap") as bmp:
    images["start"] = list(map(lambda x: x[:-1] if len(x)>=1 and x[-1]=='\n' else x, bmp.readlines()))
with open("../bitmaps/start_word.bitmap") as bmp:
    images["word"] = list(map(lambda x: x[:-1] if len(x)>=1 and x[-1]=='\n' else x, bmp.readlines()))
with open("../bitmaps/start_menu.bitmap") as bmp:
    images["menu"] = list(map(lambda x: x[:-1] if len(x)>=1 and x[-1]=='\n' else x, bmp.readlines()))
with open("../bitmaps/map.bitmap") as bmp:
    images["map"] = list(map(lambda x: x[:-1] if len(x)>=1 and x[-1]=='\n' else x, bmp.readlines()))
with open("../bitmaps/char_right.bitmap") as bmp:
    images["char"] = list(map(lambda x: x[:-1] if len(x)>=1 and x[-1]=='\n' else x, bmp.readlines()))
with open("../bitmaps/char_back.bitmap") as bmp:
    images["char_back"] = list(map(lambda x: x[:-1] if len(x)>=1 and x[-1]=='\n' else x, bmp.readlines()))
with open("../bitmaps/enemy.bitmap") as bmp:
    images["enemy"] = list(map(lambda x: x[:-1] if len(x)>=1 and x[-1]=='\n' else x, bmp.readlines()))
with open("../bitmaps/char_gg.bitmap") as bmp:
    images["chargg"] = list(map(lambda x: x[:-1] if len(x)>=1 and x[-1]=='\n' else x, bmp.readlines()))
with open("../bitmaps/bo_arrow.bitmap") as bmp:
    images["bo_arrow"] = list(map(lambda x: x[:-1] if len(x)>=1 and x[-1]=='\n' else x, bmp.readlines()))
with open("../bitmaps/bo_tail1.bitmap") as bmp:
    images["bo_tail1"] = list(map(lambda x: x[:-1] if len(x)>=1 and x[-1]=='\n' else x, bmp.readlines()))
with open("../bitmaps/bo_tail2.bitmap") as bmp:
    images["bo_tail2"] = list(map(lambda x: x[:-1] if len(x)>=1 and x[-1]=='\n' else x, bmp.readlines()))
with open("../bitmaps/simplemap.bitmap") as bmp:
    images["simplemap"] = list(map(lambda x: x[:-1] if len(x)>=1 and x[-1]=='\n' else x, bmp.readlines()))
with open("../bitmaps/success.bitmap") as bmp:
    images["success"] = list(map(lambda x: x[:-1] if len(x)>=1 and x[-1]=='\n' else x, bmp.readlines()))
with open("../bitmaps/fail.bitmap") as bmp:
    images["fail"] = list(map(lambda x: x[:-1] if len(x)>=1 and x[-1]=='\n' else x, bmp.readlines()))

DISPSTART = "DISPSTART:\n"
START = {}
addr = -1
for pix in images["start"][2:]:
    addr += 1
    if pix in START:
        START[pix].append(addr)
    else:
        START[pix] = [addr]
for i in START:
    inst = "    LLI  $1, %s\n" % (i,)
    for j in START[i]:
        inst += "    LWI  $2, %d\n" % (2147500000+j,)
        inst += "    SW   $1, $2, 0\n"
    DISPSTART += inst
DISPSTART += "    JMP $0\n"
del START

DISPSIMPLEMAP = "DISPSIMPLEMAP:\n"
SIMPLEMAP = {}
addr = -1
for pix in images["simplemap"][2:]:
    addr += 1
    if pix in SIMPLEMAP:
        SIMPLEMAP[pix].append(addr)
    else:
        SIMPLEMAP[pix] = [addr]
for i in SIMPLEMAP:
    inst = "    LLI  $1, %s\n" % (i,)
    for j in SIMPLEMAP[i]:
        inst += "    LWI  $2, %d\n" % (2147500000+j,)
        inst += "    SW   $1, $2, 0\n"
    DISPSIMPLEMAP += inst
DISPSIMPLEMAP += "    JMP $0\n"
del SIMPLEMAP

DISPWORD = "DISPWORD:\n"
WORDX = int(images["word"][0])
WORDY = int(images["word"][1])
WORDSTARTX = (OLEDX-WORDX)//2
WORDSTARTY = (OLEDY-WORDY)//2
WORD = {}
addr = -1
for pix in images["word"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in WORD:
            WORD[pix].append(addr)
        else:
            WORD[pix] = [addr]
for i in WORD:
    inst = "    LLI  $1, %s\n" % (i,)
    for j in WORD[i]:
        inst += "    LWI  $2, %d\n" % ((2147500000+WORDSTARTY*OLEDX+WORDSTARTX) + j//WORDX*OLEDX+j%WORDX,)
        inst += "    SW   $1, $2, 0\n"
    DISPWORD += inst
DISPWORD += "    JMP $0\n"
del WORD
del WORDSTARTX
del WORDSTARTY
del WORDX
del WORDY

DISPSUCCESS = "DISPSUCCESS:\n"
SUCCESSX = int(images["success"][0])
SUCCESSY = int(images["success"][1])
SUCCESSSTARTX = (OLEDX-SUCCESSX)//2
SUCCESSSTARTY = (OLEDY-SUCCESSY)//2
SUCCESS = {}
addr = -1
for pix in images["success"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in SUCCESS:
            SUCCESS[pix].append(addr)
        else:
            SUCCESS[pix] = [addr]
for i in SUCCESS:
    inst = "    LLI  $1, %s\n" % (i,)
    for j in SUCCESS[i]:
        inst += "    LWI  $2, %d\n" % ((2147500000+SUCCESSSTARTY*OLEDX+SUCCESSSTARTX) + j//SUCCESSX*OLEDX+j%SUCCESSX,)
        inst += "    SW   $1, $2, 0\n"
    DISPSUCCESS += inst
DISPSUCCESS += "    JMP $0\n"
del SUCCESS
del SUCCESSSTARTX
del SUCCESSSTARTY
del SUCCESSX
del SUCCESSY

DISPFAIL = "DISPFAIL:\n"
FAILX = int(images["fail"][0])
FAILY = int(images["fail"][1])
FAILSTARTX = (OLEDX-FAILX)//2
FAILSTARTY = (OLEDY-FAILY)//2
FAIL = {}
addr = -1
for pix in images["fail"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in FAIL:
            FAIL[pix].append(addr)
        else:
            FAIL[pix] = [addr]
for i in FAIL:
    inst = "    LLI  $1, %s\n" % (i,)
    for j in FAIL[i]:
        inst += "    LWI  $2, %d\n" % ((2147500000+FAILSTARTY*OLEDX+FAILSTARTX) + j//FAILX*OLEDX+j%FAILX,)
        inst += "    SW   $1, $2, 0\n"
    DISPFAIL += inst
DISPFAIL += "    JMP $0\n"
del FAIL
del FAILSTARTX
del FAILSTARTY
del FAILX
del FAILY

'''
#state: $1
DISPCHAR = "DISPCHAR:\n"
CHARX = int(images["chargg"][0])
CHARY = int(images["chargg"][1])
CHARSTARTX = (OLEDX-CHARX)//2
CHARSTARTY = (OLEDY-CHARY)//2
CHAR = {}   
addr = -1
for pix in images["char"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in CHAR:
            CHAR[pix].append(addr)
        else:
            CHAR[pix] = [addr]
CHARGG = {}
addr = -1
for pix in images["chargg"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in CHARGG:
            CHARGG[pix].append(addr)
        else:
            CHARGG[pix] = [addr]
CHARBACK = {}
addr = -1
for pix in images["char_back"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in CHARBACK:
            CHARBACK[pix].append(addr)
        else:
            CHARBACK[pix] = [addr]
DISPCHAR += "    BNE  $1, 0\n"
DISPCHAR += "    JUMP CHARGG\n"
DISPCHAR += "    BNE  $1, 1\n"
DISPCHAR += "    JUMP CHARLEFT\n"
DISPCHAR += "    BNE  $1, 2\n"
DISPCHAR += "    JUMP CHARLEFT\n"
DISPCHAR += "    BNE  $1, 3\n"
DISPCHAR += "    JUMP CHARRIGHT\n"
DISPCHAR += "    BNE  $1, 4\n"
DISPCHAR += "    JUMP CHARRIGHT\n"
DISPCHAR += "    BNE  $1, 5\n"
DISPCHAR += "    JUMP CHARBACK\n"
DISPCHAR += "CHARGG:\n"
for i in CHARGG:
    inst = "    LLI  $3, %s\n" % (i,)
    for j in CHARGG[i]:
        inst += "    LWI  $2, %d\n" % ((2147500000+CHARSTARTY*OLEDX+CHARSTARTX) + j//CHARX*OLEDX+j%CHARX,)
        inst += "    SW   $3, $2, 0\n"
    DISPCHAR += inst
DISPCHAR += "    JUMP CHARAFTERDEF\n"
DISPCHAR += "CHARBACK:\n"
for i in CHARBACK:
    inst = "    LLI  $3, %s\n" % (i,)
    for j in CHARBACK[i]:
        inst += "    LWI  $2, %d\n" % ((2147500000+CHARSTARTY*OLEDX+CHARSTARTX) + j//CHARX*OLEDX+j%CHARX,)
        inst += "    SW   $3, $2,  0\n"
    DISPCHAR += inst
DISPCHAR += "    JUMP CHARAFTERDEF\n"
DISPCHAR += "CHARRIGHT:\n"
for i in CHAR:
    inst = "    LLI  $3, %s\n" % (i,)
    for j in CHAR[i]:
        inst += "    LWI  $2, %d\n" % ((2147500000+CHARSTARTY*OLEDX+CHARSTARTX) + j//CHARX*OLEDX+j%CHARX,)
        inst += "    SW   $3, $2, 0\n"
    DISPCHAR += inst
DISPCHAR += "    BNE  $1, 3\n"
DISPCHAR += "    JUMP CHARRIGHT1\n"
DISPCHAR += "CHARRIGHT2:\n"
DISPCHAR += ""                                                         ###################################
DISPCHAR += "    JUMP CHARAFTERDEF\n"
DISPCHAR += "CHARRIGHT1:\n"
DISPCHAR += ""                                                         ###################################
DISPCHAR += "    JUMP CHARAFTERDEF\n"
DISPCHAR += "CHARLEFT:\n"
for i in CHAR:
    inst = "    LLI  $3, %s\n" % (i,)
    for j in CHAR[i]:
        inst += "    LWI  $2, %d\n" % ((2147500000+CHARSTARTY*OLEDX+CHARSTARTX) + (j//CHARX+1)*OLEDX-j%CHARX+CHARX,)
        inst += "    SW   $3, $2, 0\n"
    DISPCHAR += inst
DISPCHAR += "    BNE  $1, 1\n"
DISPCHAR += "    JUMP CHARLEFT1\n"
DISPCHAR += "CHARLEFT2:\n"
DISPCHAR += ""                                                         ###################################
DISPCHAR += "    JUMP CHARAFTERDEF\n"
DISPCHAR += "CHARLEFT1:\n"
DISPCHAR += ""                                                         ###################################
DISPCHAR += "    JUMP CHARAFTERDEF\n"
DISPCHAR += "CHARAFTERDEF:\n"
DISPCHAR += "    JMP  $0\n" #return
del CHAR
del CHARX
del CHARY
'''

#state: $1
#x: $2
#y: $3
DISPCHARA = "DISPCHARA:\n"
CHARX = int(images["chargg"][0])
CHARY = int(images["chargg"][1])
CHARSTARTX = (OLEDX-CHARX)//2
CHARSTARTY = (OLEDY-CHARY)//2
CHAR = {}   
addr = -1
for pix in images["char"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in CHAR:
            CHAR[pix].append(addr)
        else:
            CHAR[pix] = [addr]
CHARGG = {}
addr = -1
for pix in images["chargg"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in CHARGG:
            CHARGG[pix].append(addr)
        else:
            CHARGG[pix] = [addr]
CHARBACK = {}
addr = -1
for pix in images["char_back"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in CHARBACK:
            CHARBACK[pix].append(addr)
        else:
            CHARBACK[pix] = [addr]
DISPCHARA += "    ADDi $14, $2, 0\n"
DISPCHARA += "    ADDi $15, $3, 0\n"
DISPCHARA += "    LWI  $11, %d\n" % (OLEDX,)
DISPCHARA += "    LWI  $17, 2147500000\n"
DISPCHARA += "    BNE  $1, 0\n"
DISPCHARA += "    JUMP CHARGG\n"
DISPCHARA += "    BNE  $1, 1\n"
DISPCHARA += "    JUMP CHARLEFT\n"
DISPCHARA += "    BNE  $1, 2\n"
DISPCHARA += "    JUMP CHARLEFT\n"
DISPCHARA += "    BNE  $1, 3\n"
DISPCHARA += "    JUMP CHARRIGHT\n"
DISPCHARA += "    BNE  $1, 4\n"
DISPCHARA += "    JUMP CHARRIGHT\n"
DISPCHARA += "    BNE  $1, 5\n"
DISPCHARA += "    JUMP CHARBACK\n"
DISPCHARA += "CHARGG:\n"
for i in CHARGG:
    inst = "    LLI  $3, %s\n" % (i,)
    for j in CHARGG[i]:
        inst += "    ADDi $16, $14, %d\n" % (j %  CHARX,)
        inst += "    ADDi $10, $15, %d\n" % (j // CHARX,)
        inst += "    LWI  $9,  LINE_NUMBER+5\n"
        inst += "    JUMP MULTIPLICATION\n"
        inst += "    ADD  $2, $12, $16\n"    #OLEDADDR
        inst += "    ADD  $2, $2,  $17\n"
        inst += "    SW   $3, $2,  0\n"
    DISPCHARA += inst
DISPCHARA += "    JUMP CHARAFTERDEF\n"
DISPCHARA += "CHARBACK:\n"
for i in CHARBACK:
    inst = "    LLI  $3, %s\n" % (i,)
    for j in CHARBACK[i]:
        inst += "    ADDi $16, $14, %d\n" % (j %  CHARX,)
        inst += "    ADDi $10, $15, %d\n" % (j // CHARX,)
        inst += "    LWI  $9,  LINE_NUMBER+5\n"
        inst += "    JUMP MULTIPLICATION\n"
        inst += "    ADD  $2, $12, $16\n"    #OLEDADDR
        inst += "    ADD  $2, $2,  $17\n"
        inst += "    SW   $3, $2,  0\n"
    DISPCHARA += inst
DISPCHARA += "    JUMP CHARAFTERDEF\n"
DISPCHARA += "CHARRIGHT:\n"
for i in CHAR:
    inst = "    LLI  $3, %s\n" % (i,)
    for j in CHAR[i]:
        inst += "    ADDi $16, $14, %d\n" % (j % CHARX,)
        inst += "    ADDi $10, $15, %d\n" % (j // CHARX,)
        inst += "    LWI  $9,  LINE_NUMBER+5\n"
        inst += "    JUMP MULTIPLICATION\n"
        inst += "    ADD  $2, $12, $16\n"    #OLEDADDR
        inst += "    ADD  $2, $2,  $17\n"
        inst += "    SW   $3, $2, 0\n"
    DISPCHARA += inst
DISPCHARA += "    BNE  $1, 3\n"
DISPCHARA += "    JUMP CHARRIGHT1\n"
DISPCHARA += "CHARRIGHT2:\n"
DISPCHARA += ""                                                         ###################################
DISPCHARA += "    JUMP CHARAFTERDEF\n"
DISPCHARA += "CHARRIGHT1:\n"
DISPCHARA += ""                                                         ###################################
DISPCHARA += "    JUMP CHARAFTERDEF\n"
DISPCHARA += "CHARLEFT:\n"
for i in CHAR:
    inst = "    LLI  $3, %s\n" % (i,)
    for j in CHAR[i]:
        inst += "    ADDi $16, $14, %d\n" % (CHARX - j % CHARX,)
        inst += "    ADDi $10, $15, %d\n" % (j // CHARX,)
        inst += "    LWI  $9,  LINE_NUMBER+5\n"
        inst += "    JUMP MULTIPLICATION\n"
        inst += "    ADD  $2, $12, $16\n"    #OLEDADDR
        inst += "    ADD  $2, $2,  $17\n"
        inst += "    SW   $3, $2, 0\n"
    DISPCHARA += inst
DISPCHARA += "    BNE  $1, 1\n"
DISPCHARA += "    JUMP CHARLEFT1\n"
DISPCHARA += "CHARLEFT2:\n"
DISPCHARA += ""                                                         ###################################
DISPCHARA += "    JUMP CHARAFTERDEF\n"
DISPCHARA += "CHARLEFT1:\n"
DISPCHARA += ""                                                         ###################################
DISPCHARA += "    JUMP CHARAFTERDEF\n"
DISPCHARA += "CHARAFTERDEF:\n"
DISPCHARA += "    JMP  $0\n" #return
del CHAR
del CHARX
del CHARY


#centre_x: $1, centre_y: $2
DISPMAP = "DISPMAP:\n"
MAPSCALEEXP = 4 # coord>>4
MAPX = int(images["map"][0])
MAPY = int(images["map"][1])
DISPMAP += "    LWI  $10, 0\n"                       #$10 = oled addr_offset
DISPMAP += "    LWI  $20, 2147500000\n"              #$20 = oled_addr_base
DISPMAP += "DISPMAPLOOP:\n"
DISPMAP += "    LWI  $11, %d\n" % (OLEDX,)           #$11 = OLEDX
DISPMAP += "    LWI  $9,  LINE_NUMBER+5\n"           #Return addr
DISPMAP += "    JUMP MODULUS\n"                      #$12 = $10 % $11
DISPMAP += "    ADDi $15, $12, 0\n"                  #$15 = result
DISPMAP += "    LWI  $16, 1\n"                       #$16 = 1
DISPMAP += "    SRL  $16, $11, $16\n"                #$16 = OLEDX >> 1
DISPMAP += "    SUB  $15, $15, $16\n"                #x_offset
DISPMAP += "    LWI  $9,  LINE_NUMBER+5\n"           #Return addr
DISPMAP += "    JUMP DIVISION\n"                     #$12 = $10 / $11
DISPMAP += "    ADDi $16, $12, 0\n"                  #$16 = result
DISPMAP += "    LWI  $17, %d\n" % (OLEDY,)           #$17 = OLEDY
DISPMAP += "    LWI  $18, 1\n"                       #$18 = 1
DISPMAP += "    SRL  $17, $17, $18\n"                #$17 = OLEDY >> 1
DISPMAP += "    SUB  $16, $16, $17\n"                #y_offset
DISPMAP += "    ADDi $10, $10, 1\n"                  #$10 ++; increment addr
DISPMAP += "    ADD  $3,  $1,  $15\n"                #$3 = x coord on big map
DISPMAP += "    ADD  $4,  $2,  $16\n"                #$4 = y_coord on big map
DISPMAP += "    LWI  $5,  %d\n" % (MAPSCALEEXP,)     #scale factor as power of 2
DISPMAP += "    SRL  $3,  $3,  $5\n"                 #$3 = x_coord on small map
DISPMAP += "    SRL  $4,  $4,  $5\n"                 #$4 = y_coord on small map
DISPMAP += "    LWI  $5,  LINE_NUMBER+5\n"           #return_addr for GETMAPCOLOR
DISPMAP += "    JUMP GETMAPCOLOR\n"                  #$6 = color
DISPMAP += "    ADD  $5,  $10, $20\n"                  #pix addr in memory
DISPMAP += "    SW   $6,  $5,  0\n"                  #Draw pixel
DISPMAP += "    BEQ  $10, %d\n" % (OLEDX*OLEDY,)     #If end of oled reached, skip next line
DISPMAP += "    JUMP DISPMAPLOOP\n"                  #GOTO DISPMAPLOOP
DISPMAP += "    JMP  $0\n"                           #Return...

#x_cooord: $3, y_coord: $4
#return addr: $5
GETMAPCOLOR = "GETMAPCOLOR:\n"
for i in range(MAPX):
    inst  = "    BNE  $3, %d\n" % (i,)
    inst += "    JUMP MAPX%d\n" % (i,)
    GETMAPCOLOR += inst
GETMAPCOLOR += "    LWI  $6, 0\n    JMP  $5\n" #Return black if x out of range
for i in range(MAPX):
    inst  = "MAPX%d:\n" % (i,)
    for j in range(MAPY):
        inst += "    BNE  $4, %d\n" % (j,)
        inst += "    LWI  $6, %s\n" % (images["map"][2+j*MAPX+i],)
    inst += "    JMP  $5\n"
    GETMAPCOLOR += inst
del MAPX
del MAPY
del MAPSCALEEXP

#centre_x: $1, centre_y: $2
#enemy_x:  $3, enemy_y:  $4 (top left corner)
DISPENEMY = "DISPENEMY:\n"
ENEMYX = int(images["enemy"][0])
ENEMYY = int(images["enemy"][1])
ENEMY = {}
addr = -1
for pix in images["enemy"][2:]:
    addr += 1
    if eval(pix) != 0:
        if pix in ENEMY:
            ENEMY[pix].append(addr)
        else:
            ENEMY[pix] = [addr]
DISPENEMY += "    LWI  $13, 1 \n"                        #$13 = constant 1
DISPENEMY += "    LWI  $14, %d\n" % (OLEDX,)             #$14 = OLEDX
DISPENEMY += "    LWI  $15, %d\n" % (OLEDY,)             #$15 = OLEDY
DISPENEMY += "    SRL  $16,  $14, $13\n"                 #$16 = OLEDX >> 1
for i in ENEMY:
    inst = "    LLI  $16, %s\n" % (i,)                   #$16 = color
    for j in ENEMY[i]:
        inst += "    SUB  $6,  $3,  $1 \n"               #$6 = EX - CX
        inst += "    ADD  $5,  $6,  $16\n"               #$5 = $6 + $16 (EXscr)
        inst += "    SUB  $7,  $4,  $2 \n"               #$7 = EY - CY
        inst += "    ADD  $6,  $7,  $16\n"               #$6 = $7 + $16 (EYscr)
        inst += "    ADDi $5,  $5,  %d\n" % (j% ENEMYX,) #$5 = Pix_x
        inst += "    ADDi $6,  $6,  %d\n" % (j//ENEMYX,) #$6 = Pix_y
        inst += "    SLT  $7,  $5,  $14\n"               #$7 = Pix_x < OLEDX
        inst += "    SLT  $8,  $6,  $15\n"               #$8 = Pix_y < OLEDY
        inst += "    BEQ  $7,  1\n"                      #if within boundary, skip next
        inst += "    JUMP %s\n" % ("DISPENEMY%s%sEND" % (i[2:], j,),)
        inst += "    BEQ  $8,  1\n"                      #if within boundary, skip next
        inst += "    JUMP %s\n" % ("DISPENEMY%s%sEND" % (i[2:], j,),)
        inst += "    ADDi $10, $6, 0\n"                  #$10 = Pix_y
        inst += "    LWI  $11, %d\n" % (ENEMYX,)         #$11 = ENEMYX
        inst += "    LWI  $9,  LINE_NUMBER+5\n"          #$9 = Return addr
        inst += "    JUMP MULTIPLICATION\n"              #$12 = $10 * $11
        inst += "    ADD  $12, $12, $5\n"                #$12 = Pix_addr
        inst += "    SW   $16, $12, 0\n"                 #Draw $16 at $12
        inst += "DISPENEMY%s%sEND:\n" % (i[2:], j,)
    DISPENEMY += inst
DISPENEMY += "    JMP  $0\n"
del ENEMY
del ENEMYX
del ENEMYY


DISPBO = "DISPBO:\n"


#$1: top_left_coord({[15:0] x, [15:0] y})
#$2: color
#$3: ASCII (support 'd32 - 'd126)
#  each char is 3x5
#  from: https://hackaday.io/project/6309-vga-graphics-over-spi-and-serial-vgatonic/log/20759-a-tiny-4x6-pixel-font-that-will-fit-on-almost-any-microcontroller-license-mit
DISPCH = '''DISPCH:
    BNE  $3, 32  //space
    JUMP  DISPCHspace
    BNE  $3, 33  //!
    JUMP  DISPCH!
    BNE  $3, 34  //"
    JUMP  DISPCH"
    BNE  $3, 35  //#
    JUMP  DISPCH#
    BNE  $3, 36  //$
    JUMP  DISPCH$
    BNE  $3, 37  //%
    JUMP  DISPCH%
    BNE  $3, 38  //&
    JUMP  DISPCH&
    BNE  $3, 39  //'
    JUMP  DISPCH'
    BNE  $3, 40  //(
    JUMP  DISPCH(
    BNE  $3, 41  //)
    JUMP  DISPCH)
    BNE  $3, 42  //*
    JUMP  DISPCH*
    BNE  $3, 43  //+
    JUMP  DISPCH+
    BNE  $3, 44  //,
    JUMP  DISPCHcomma
    BNE  $3, 45  //-
    JUMP  DISPCH-
    BNE  $3, 46  //.
    JUMP  DISPCH.
    BNE  $3, 47  ///
    JUMP  DISPCH/
    BNE  $3, 48  //0
    JUMP  DISPCH0
    BNE  $3, 49  //1
    JUMP  DISPCH1
    BNE  $3, 50  //2
    JUMP  DISPCH2
    BNE  $3, 51  //3
    JUMP  DISPCH3
    BNE  $3, 52  //4
    JUMP  DISPCH4
    BNE  $3, 53  //5
    JUMP  DISPCH5
    BNE  $3, 54  //6
    JUMP  DISPCH6
    BNE  $3, 55  //7
    JUMP  DISPCH7
    BNE  $3, 56  //8
    JUMP  DISPCH8
    BNE  $3, 57  //9
    JUMP  DISPCH9
    BNE  $3, 58  //:
    JUMP  DISPCHcolon
    BNE  $3, 59  //;
    JUMP  DISPCH;
    BNE  $3, 60  //<
    JUMP  DISPCH<
    BNE  $3, 61  //=
    JUMP  DISPCH=
    BNE  $3, 62  //>
    JUMP  DISPCH>
    BNE  $3, 63  //?
    JUMP  DISPCH?
    BNE  $3, 64  //@
    JUMP  DISPCH@
    BNE  $3, 65  //A
    JUMP  DISPCHA
    BNE  $3, 66  //B
    JUMP  DISPCHB
    BNE  $3, 67  //C
    JUMP  DISPCHC
    BNE  $3, 68  //D
    JUMP  DISPCHD
    BNE  $3, 69  //E
    JUMP  DISPCHE
    BNE  $3, 70  //F
    JUMP  DISPCHF
    BNE  $3, 71  //G
    JUMP  DISPCHG
    BNE  $3, 72  //H
    JUMP  DISPCHH
    BNE  $3, 73  //I
    JUMP  DISPCHI
    BNE  $3, 74  //J
    JUMP  DISPCHJ
    BNE  $3, 75  //K
    JUMP  DISPCHK
    BNE  $3, 76  //L
    JUMP  DISPCHL
    BNE  $3, 77  //M
    JUMP  DISPCHM
    BNE  $3, 78  //N
    JUMP  DISPCHN
    BNE  $3, 79  //O
    JUMP  DISPCHO
    BNE  $3, 80  //P
    JUMP  DISPCHP
    BNE  $3, 81  //Q
    JUMP  DISPCHQ
    BNE  $3, 82  //R
    JUMP  DISPCHR
    BNE  $3, 83  //S
    JUMP  DISPCHS
    BNE  $3, 84  //T
    JUMP  DISPCHT
    BNE  $3, 85  //U
    JUMP  DISPCHU
    BNE  $3, 86  //V
    JUMP  DISPCHV
    BNE  $3, 87  //W
    JUMP  DISPCHW
    BNE  $3, 88  //X
    JUMP  DISPCHX
    BNE  $3, 89  //Y
    JUMP  DISPCHY
    BNE  $3, 90  //Z
    JUMP  DISPCHZ
    BNE  $3, 91  //[
    JUMP  DISPCH[
    BNE  $3, 92  //\\
    JUMP  DISPCH\\
    BNE  $3, 93  //]
    JUMP  DISPCH]
    BNE  $3, 94  //^
    JUMP  DISPCH^
    BNE  $3, 95  //_
    JUMP  DISPCH_
    BNE  $3, 96  //`
    JUMP  DISPCH`
    BNE  $3, 97  //a
    JUMP  DISPCHa
    BNE  $3, 98  //b
    JUMP  DISPCHb
    BNE  $3, 99  //c
    JUMP  DISPCHc
    BNE  $3, 100 //d
    JUMP  DISPCHd
    BNE  $3, 101 //e
    JUMP  DISPCHe
    BNE  $3, 102 //f
    JUMP  DISPCHf
    BNE  $3, 103 //g
    JUMP  DISPCHg
    BNE  $3, 104 //h
    JUMP  DISPCHh
    BNE  $3, 105 //i
    JUMP  DISPCHi
    BNE  $3, 106 //j
    JUMP  DISPCHj
    BNE  $3, 107 //k
    JUMP  DISPCHk
    BNE  $3, 108 //l
    JUMP  DISPCHl
    BNE  $3, 109 //m
    JUMP  DISPCHm
    BNE  $3, 110 //n
    JUMP  DISPCHn
    BNE  $3, 111 //o
    JUMP  DISPCHo
    BNE  $3, 112 //p
    JUMP  DISPCHp
    BNE  $3, 113 //q
    JUMP  DISPCHq
    BNE  $3, 114 //r
    JUMP  DISPCHr
    BNE  $3, 115 //s
    JUMP  DISPCHs
    BNE  $3, 116 //t
    JUMP  DISPCHt
    BNE  $3, 117 //u
    JUMP  DISPCHu
    BNE  $3, 118 //v
    JUMP  DISPCHv
    BNE  $3, 119 //w
    JUMP  DISPCHw
    BNE  $3, 120 //x
    JUMP  DISPCHx
    BNE  $3, 121 //y
    JUMP  DISPCHy
    BNE  $3, 122 //z
    JUMP  DISPCHz
    BNE  $3, 123 //{
    JUMP  DISPCH{
    BNE  $3, 124 //|
    JUMP  DISPCH|
    BNE  $3, 125 //}
    JUMP  DISPCH}
    BNE  $3, 126 //~
    JUMP  DISPCH~
DISPCHspace:
    LLI  $4, 0b000000000000000
    JUMP DISPCHDRAW
DISPCH!:
    LLI  $4, 0b010010010000010
    JUMP DISPCHDRAW
DISPCH":
    LLI  $4, 0b101101000000000
    JUMP DISPCHDRAW
DISPCH#:
    LLI  $4, 0b101111101111101
    JUMP DISPCHDRAW
DISPCH$:
    LLI  $4, 0b011110111011110
    JUMP DISPCHDRAW
DISPCH%:
    LLI  $4, 0b101001010100101
    JUMP DISPCHDRAW
DISPCH&:
    LLI  $4, 0b010101010101110
    JUMP DISPCHDRAW
DISPCH':
    LLI  $4, 0b010010000000000
    JUMP DISPCHDRAW
DISPCH(:
    LLI  $4, 0b001010010010001
    JUMP DISPCHDRAW
DISPCH):
    LLI  $4, 0b100010010010100
    JUMP DISPCHDRAW
DISPCH*:
    LLI  $4, 0b000101010101000
    JUMP DISPCHDRAW
DISPCH+:
    LLI  $4, 0b000010111010000
    JUMP DISPCHDRAW
DISPCHcomma:
    LLI  $4, 0b000000000010100
    JUMP DISPCHDRAW
DISPCH-:
    LLI  $4, 0b000000111000000
    JUMP DISPCHDRAW
DISPCH.:
    LLI  $4, 0b000000000000010
    JUMP DISPCHDRAW
DISPCH/:
    LLI  $4, 0b001001010100100
    JUMP DISPCHDRAW
DISPCH0:
    LLI  $4, 0b010101101101010
    JUMP DISPCHDRAW
DISPCH1:
    LLI  $4, 0b010110010010111
    JUMP DISPCHDRAW
DISPCH2:
    LLI  $4, 0b111001010100111
    JUMP DISPCHDRAW
DISPCH3:
    LLI  $4, 0b110001111001110
    JUMP DISPCHDRAW
DISPCH4:
    LLI  $4, 0b001011101111001
    JUMP DISPCHDRAW
DISPCH5:
    LLI  $4, 0b111100110001110
    JUMP DISPCHDRAW
DISPCH6:
    LLI  $4, 0b011100110101010
    JUMP DISPCHDRAW
DISPCH7:
    LLI  $4, 0b111001010010010
    JUMP DISPCHDRAW
DISPCH8:
    LLI  $4, 0b111101010101111
    JUMP DISPCHDRAW
DISPCH9:
    LLI  $4, 0b010101011001111
    JUMP DISPCHDRAW
DISPCHcolon:
    LLI  $4, 0b000010000010000
    JUMP DISPCHDRAW
DISPCH;:
    LLI  $4, 0b000010000010100
    JUMP DISPCHDRAW
DISPCH<:
    LLI  $4, 0b001010100010001
    JUMP DISPCHDRAW
DISPCH=:
    LLI  $4, 0b000111000111000
    JUMP DISPCHDRAW
DISPCH>:
    LLI  $4, 0b100010001010100
    JUMP DISPCHDRAW
DISPCH?:
    LLI  $4, 0b111001010000010
    JUMP DISPCHDRAW
DISPCH@:
    LLI  $4, 0b010101101100011
    JUMP DISPCHDRAW
DISPCHA:
    LLI  $4, 0b011101111101101
    JUMP DISPCHDRAW
DISPCHB:
    LLI  $4, 0b011101110101110
    JUMP DISPCHDRAW
DISPCHC:
    LLI  $4, 0b011100100100011
    JUMP DISPCHDRAW
DISPCHD:
    LLI  $4, 0b110101101101110
    JUMP DISPCHDRAW
DISPCHE:
    LLI  $4, 0b011100111100111
    JUMP DISPCHDRAW
DISPCHF:
    LLI  $4, 0b011100111100100
    JUMP DISPCHDRAW
DISPCHG:
    LLI  $4, 0b011100101101011
    JUMP DISPCHDRAW
DISPCHH:
    LLI  $4, 0b101101111101101
    JUMP DISPCHDRAW
DISPCHI:
    LLI  $4, 0b111010010010111
    JUMP DISPCHDRAW
DISPCHJ:
    LLI  $4, 0b011001001101010
    JUMP DISPCHDRAW
DISPCHK:
    LLI  $4, 0b101101110101101
    JUMP DISPCHDRAW
DISPCHL:
    LLI  $4, 0b100100100100111
    JUMP DISPCHDRAW
DISPCHM:
    LLI  $4, 0b101111101101101
    JUMP DISPCHDRAW
DISPCHN:
    LLI  $4, 0b110101101101101
    JUMP DISPCHDRAW
DISPCHO:
    LLI  $4, 0b010101101101010
    JUMP DISPCHDRAW
DISPCHP:
    LLI  $4, 0b110101111100100
    JUMP DISPCHDRAW
DISPCHQ:
    LLI  $4, 0b011101101111011
    JUMP DISPCHDRAW
DISPCHR:
    LLI  $4, 0b011101110101101
    JUMP DISPCHDRAW
DISPCHS:
    LLI  $4, 0b011100010001110
    JUMP DISPCHDRAW
DISPCHT:
    LLI  $4, 0b111010010010010
    JUMP DISPCHDRAW
DISPCHU:
    LLI  $4, 0b101101101101011
    JUMP DISPCHDRAW
DISPCHV:
    LLI  $4, 0b101101101101010
    JUMP DISPCHDRAW
DISPCHW:
    LLI  $4, 0b101101101111101
    JUMP DISPCHDRAW
DISPCHX:
    LLI  $4, 0b101101010101101
    JUMP DISPCHDRAW
DISPCHY:
    LLI  $4, 0b101101010010010
    JUMP DISPCHDRAW
DISPCHZ:
    LLI  $4, 0b111001010100111
    JUMP DISPCHDRAW
DISPCH[:
    LLI  $4, 0b011010010010011
    JUMP DISPCHDRAW
DISPCH\\:
    LLI  $4, 0b100100010001001
    JUMP DISPCHDRAW
DISPCH]:
    LLI  $4, 0b110010010010110
    JUMP DISPCHDRAW
DISPCH^:
    LLI  $4, 0b010101000000000
    JUMP DISPCHDRAW
DISPCH_:
    LLI  $4, 0b000000000000111
    JUMP DISPCHDRAW
DISPCH`:
    LLI  $4, 0b010001000000000
    JUMP DISPCHDRAW
DISPCHa:
    LLI  $4, 0b000011101101011
    JUMP DISPCHDRAW
DISPCHb:
    LLI  $4, 0b100110101101110
    JUMP DISPCHDRAW
DISPCHc:
    LLI  $4, 0b0000111100100011
    JUMP DISPCHDRAW
DISPCHd:
    LLI  $4, 0b001011101101011
    JUMP DISPCHDRAW
DISPCHe:
    LLI  $4, 0b000011101110011
    JUMP DISPCHDRAW
DISPCHf:
    LLI  $4, 0b010101100110100
    JUMP DISPCHDRAW
DISPCHg:
    LLI  $4, 0b010101011001110
    JUMP DISPCHDRAW
DISPCHh:
    LLI  $4, 0b100100110101101
    JUMP DISPCHDRAW
DISPCHi:
    LLI  $4, 0b010000010010001
    JUMP DISPCHDRAW
DISPCHj:
    LLI  $4, 0b010000010010100
    JUMP DISPCHDRAW
DISPCHk:
    LLI  $4, 0b100101110101101
    JUMP DISPCHDRAW
DISPCHl:
    LLI  $4, 0b010010010010001
    JUMP DISPCHDRAW
DISPCHm:
    LLI  $4, 0b000101111101101
    JUMP DISPCHDRAW
DISPCHn:
    LLI  $4, 0b000110101101101
    JUMP DISPCHDRAW
DISPCHo:
    LLI  $4, 0b000010101101010
    JUMP DISPCHDRAW
DISPCHp:
    LLI  $4, 0b110101101110100
    JUMP DISPCHDRAW
DISPCHq:
    LLI  $4, 0b011101101011001
    JUMP DISPCHDRAW
DISPCHr:
    LLI  $4, 0b000101110100100
    JUMP DISPCHDRAW
DISPCHs:
    LLI  $4, 0b000011110001110
    JUMP DISPCHDRAW
DISPCHt:
    LLI  $4, 0b100110100100011
    JUMP DISPCHDRAW
DISPCHu:
    LLI  $4, 0b000101101101011
    JUMP DISPCHDRAW
DISPCHv:
    LLI  $4, 0b000101101101110
    JUMP DISPCHDRAW
DISPCHw:
    LLI  $4, 0b000101101111101
    JUMP DISPCHDRAW
DISPCHx:
    LLI  $4, 0b000101010101101
    JUMP DISPCHDRAW
DISPCHy:
    LLI  $4, 0b101101011001010
    JUMP DISPCHDRAW
DISPCHz:
    LLI  $4, 0b000111001010111
    JUMP DISPCHDRAW
DISPCH{:
    LLI  $4, 0b011010110010011
    JUMP DISPCHDRAW
DISPCH|:
    LLI  $4, 0b010010010010010
    JUMP DISPCHDRAW
DISPCH}:
    LLI  $4, 0b110010011010110
    JUMP DISPCHDRAW
DISPCH~:
    LLI  $4, 0b000000010101000
    JUMP DISPCHDRAW
DISPCHDRAW:
    LWI  $5, 2147500000
    LWI  $6, 16
    SLL  $7, $1, $6
    SRL  $7, $7, $6                  //y_coord of tl
    SRL  $6, $1, $6                  //x_coord of tl
    LWI  $19, ''' + str(OLEDX) + ''' //OLEDX
    LWI  $20, ''' + str(OLEDY) + ''' //OLEDY
    LWI  $21, 0                      //$21 = y_coord of font
    ADDi $13, $7, 0                  //$13 = y_coord
    LWI  $22, 31                     //constant 31
DISPCHLINLOOP:
    BNE  $21, 5                      //y_coord==5 -> out of bound
    JUMP DISPCHENDL
    ADDi $14, $6, 0                  //$14 = x_coord
    LWI  $22, 0                      //$22 = x_coord of font
DISPCHCOLLOOP:
    BNE  $22, 3                      //x_coord==3 -> out of bound
    JUMP DISPCHCOLLOOPEND
    SLT  $15, $14, $19               //x on oled?
    SLT  $16, $13, $20               //y on oled?
    BEQ  $15, 1                      //if not
    JUMP DISPCHCOLLOOPEND            //next line
    BEQ  $16, 1                      //if not
    JUMP DISPCHENDL                  //exit function
    ADDi $10, $19, 0                 //OLEDX
    ADDi $11, $13, 0                 //y_coord
    LWI  $9,  LINE_NUMBER+5          //return addr of multiplication function
    JUMP MULTIPLICATION              //$12 = OLEDX * y_coord
    ADD  $12, $12, $14               //$12 = pix mem addr
    ADD  $9,  $21, $21
    ADD  $9,  $9,  $21               //$9 = $21*3
    ADD  $9,  $9,  $22               //$9 = bit position
    SRL  $9,  $4,  $9
    SLL  $9,  $9,  $22
    SRL  $9,  $9,  $22               //$9 = bit
    BEQ  $9,  0                      //if (bit==0): skip next
    SW   $2,  $12, 0                 //Draw pixel
DISPCHCOLEND:
    ADDi $14, $14, 1                 //x_coord++
    ADDi $22, $22, 1
    JUMP DISPCHCOLLOOP
DISPCHCOLLOOPEND:
    ADDi $13, $13, 1                 //y_coord++
    ADDi $21, $21, 1
    JUMP DISPCHLINLOOP
DISPCHENDL:
    JMP  $0
'''

BLINK = '''BLINK:
    LWI  $3, 2147483648
    LLI  $1, 0b1010101010101010
BLINKLOOP:
    INV  $1, $1
    SW   $1, $3, 0
    LWI  $2, %d
BLINKDEL:
    SUBI $2, $2, 1
    BEQ  $2, 0
    JUMP BLINKDEL
    JUMP BLINKLOOP
''' % (int(1 * CPU_FREQ / 6),)

CHECKVOLUME = '''CHECKVOLUME:
    LWI  $2, 2147483650
    LW   $2, $2, 0
    LWI  $3, 16
    SRL  $2, $2, $3
    ANDi $2, $2, 0b0000000000001111
    BEQ  $2, 15
    JMP  $0
    JMP  $1
'''

#a//b = c
#return_addr: $9
#a: $10, b: $11, c: $12
DIVISION = '''DIVISION:
    LWI  $12, 0
    LWI  $13, 0
DIVISIONLOOP:
    ADD  $13, $13, $11
    SLT  $14, $10, $13
    BNE  $14, 1
    JMP  $9
    ADDi $12, $12, 1
    JUMP DIVISIONLOOP
'''

#a%b = c
#return_addr: $9
#a: $10, b: $11, c: $12
MODULUS = '''MODULUS:
    LWI  $12, 0
MODULUSLOOP:
    ADD  $12, $12, $11
    SLT  $13, $10, $12
    BNE  $13, 1
    JUMP MODULUSFIN
    JUMP MODULUSLOOP
MODULUSFIN:
    SUB  $12, $12, $11
    SUB  $12, $10, $12
    JMP  $9
'''

#a*b = c
#return_addr: $9
#a: $10, b: $11, c: $12
MULTIPLICATION = '''MULTIPLICATION:
    LWI  $12, 0
    ADDi $13, $11, 0
MULTIPLICATIONLOOP:
    SUBi $13, $13, 1
    ADD  $12, $12, $10
    BNE  $13, 0
    JMP  $9
    JUMP  MULTIPLICATIONLOOP
'''

#TODO:
#$1: top_left_coord({[15:0] x, [15:0] y})
#$2: color
#$3: size({[15:0] length, [15:0] width})
DRAWRECT = '''DRAWRECT:
    LWI  $15, 16
    SLL  $4,  $1,  $15
    SRL  $4,  $4,  $15    //x_coord_tl
    SRL  $5,  $1,  $15    //y_coord_tl
    JMP  $0
'''

del i
del j
del inst
del images

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        print(ABOUT)
        print(eval(input()))
    else:
        print(eval(' '.join(sys.argv[1:])))
