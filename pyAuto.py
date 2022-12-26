# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 19:58:34 2021

@author: aserpa
"""

import pyautogui as pg
import random
import os
import time

vCaminhoPaint = "C:\WINDOWS\system32\mspaint.exe"
os.startfile(vCaminhoPaint)

time.sleep(1)

wh = pg.size()
#print(wh)
vPosIniH = wh[0]/2
vPosIniV = wh[1]/2

pg.mouseDown()

#v1 = 100
#v2 = 200

x = 1
for i in range(10):
    
    v1 = random.randint(300, 700)

    pg.moveTo(v1, v1, duration=0.15)
    pg.dragTo(v1, v1, duration=0.15, button='left')
    pg.dragTo(v1 - 100, v1, duration=0.15, button='left')
    pg.dragTo(v1 - 100, v1 - 100, duration=0.15, button='left')
    pg.dragTo(v1, v1 - 100, duration=0.15, button='left')
    pg.dragTo(v1, v1, duration=0.15, button='left')

    

    
    #while x < 100:
    #    pg.dragTo(100 + x, 550 - x/4, duration=1, button='left')
    #    x = x + 10


