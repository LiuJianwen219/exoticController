# -*- coding:utf-8 -*-
import json
import random
import time

from config import *
from util.contants import *

# statement of the fpga and rpi

class RPI:

    state = 0
    SWState  = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
    BTNState = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    SEGState = [0, 0, 2, 3, 4, 5, 6, 7]
    LEDState = [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def init(self):
        if deploy == 'DEV':
            logger.debug('Function "rpi.init()" called in development mode.')
            return
        wiringpi.wiringPiSetup()
        for pin in RPI_INPUTS:
            wiringpi.pinMode(pin, wiringpi.INPUT)
            wiringpi.pullUpDnControl(pin, wiringpi.PUD_UP)
        for pin in RPI_OUTPUTS:
            wiringpi.pinMode(pin, wiringpi.OUTPUT)
            wiringpi.digitalWrite(pin, 0)
        wiringpi.setPadDrive(0, 7)
        wiringpi.digitalWrite(LCD_CTRL, 1)
        self.serial_port = serial.Serial(SERIAL_DEV, **uart_opts)
        logger.info('GPIO ports initialization done.')

    def open_SW(self, index):
        self.SWState[index] = 1

    def close_SW(self, index):
        self.SWState[index] = 0

    def press_BTN(self, index):
        self.BTNState[index] = 1

    def release_BTN(self, index):
        self.BTNState[index] = 0

    def sendPS2(self, byte):
        print("send " + byte)

    def programBit(self):
        print("program Bit, path: " + "temp/")

    def getSEG(self):
        for i in range(0, 8):
            self.SEGState[i] = (self.SEGState[i] + random.randint(0, 8)) % 8
        return self.SEGState

    def getLED(self):
        for i in range(0, 16):
            self.LEDState[i] = (self.LEDState[i] + random.randint(0, 16)) % 2
        return self.LEDState

rpi = RPI()