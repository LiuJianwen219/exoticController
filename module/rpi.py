# -*- coding:utf-8 -*-
import json
import random
import time

from config import deviceNum
from util.contants import *

# statement of the fpga and rpi
state = 0
SWState  = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
BTNState = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
SEGState = [0, 0, 2, 3, 4, 5, 6, 7]
LEDState = [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def open_SW(index):
    SWState[index] = 1

def close_SW(index):
    SWState[index] = 0

def press_BTN(index):
    BTNState[index] = 1

def release_BTN(index):
    BTNState[index] = 0

def sendPS2(byte):
    print("send " + byte)

def programBit():
    print("program Bit, path: " + "temp/")

def getSEG():
    global SEGState
    for i in range(0, 8) :
        SEGState[i] = (SEGState[i] + random.randint(0, 8)) % 8
    return SEGState

def getLED():
    global LEDState
    for i in range(0, 16):
        LEDState[i] = (LEDState[i] + random.randint(0, 16)) % 2
    return LEDState

