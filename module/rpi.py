# -*- coding:utf-8 -*-
import random
import time
import wiringpi

from config import *
from module import fpga
from util.contants import *

# ALL_GPIO = [0, 1, 2, 3, 4, 5, 6, 7, 21, 22, 23, 24, 25, 26, 27, 28, 29]
# SDA_1 = [8]
# SCL_1 = [9]
# CE01 = [10, 11]
# MIOSIO = [12, 13]
# SCLK = [14]
# TxDRxD = [15, 16]
# SDA_0 = [30]
# SCL_0 = [31]


SWITCHES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
BUTTONS  = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

BUTTONS_IN = [4, 5, 6, 7]
BUTTONS_OUT = [0, 1, 2, 3]

SER_595 = 24
CLK_595 = 25

PS2_CLK_PIN = 28
PS2_DAT_PIN = 29

RPI_INPUTS  = [4, 5, 6, 7, 26, 27, 28, 29, 31]
RPI_OUTPUTS = [0, 1, 2, 3, 24, 25, 11]

SEGLED_DATA = [26, 27, 28, 29, 31]
SEGLED_CLK = 11



logger = logging.getLogger('rpi.' + __name__)


class RPI:
    # statement of the fpga and rpi
    state = 0
    SWState = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    BTNState = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    SEGState = [0, 1, 0, 0, 0, 0, 0, 0]
    LEDState = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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
        # wiringpi.setPadDrive(0, 7) # 设置引脚组的驱动能力。设置引脚组 0的驱动能力为 7，也就是驱动能力最大
        # wiringpi.digitalWrite(LCD_CTRL, 1)
        # self.serial_port = serial.Serial(SERIAL_DEV, **uart_opts)
        self._BUTTON_INIT() # 初始化 BUTTON 输出为 1
        self._SWITCH_INIT() # 程序启动时，初始化 SW 的状态为全 0
        self._READ_DATA_INIT() # 初始化读取数据的时钟
        logger.info('GPIO ports initialization done.')

    def setStateBusy(self):
        self.state = 1

    def setStateFree(self):
        self.state = 0

    def getRPIState(self):
        return self.state


    def _BUTTON_INIT(self):
        write(BUTTONS_OUT[0], 1)
        write(BUTTONS_OUT[1], 1)
        write(BUTTONS_OUT[2], 1)
        write(BUTTONS_OUT[3], 1)

    def _SWITCH_INIT(self):
        self._WRITE_SN74HC595()

    def _READ_DATA_INIT(self):
        write(SEGLED_CLK, 1)


    def open_SW(self, index):
        if index not in SWITCHES:
            logger.error("sw index error {}".format(index))
            return
        if deploy == "DEV":
            logger.info("DEV: SW_mode:595 open sw {}".format(index))
            return
        else:
            self.SWState[index] = 1
            self._WRITE_SN74HC595()

    def close_SW(self, index):
        if index not in SWITCHES:
            logger.error("sw index error {}".format(index))
            return
        if deploy == "DEV":
            logger.info("DEV: SW_mode:595 close sw {}".format(index))
            return
        else:
            self.SWState[index] = 0
            self._WRITE_SN74HC595()

    def press_BTN(self, index):
        if index not in BUTTONS:
            logger.error("btn index error {}".format(index))
            return
        if deploy == "DEV":
            logger.info("DEV: press btn {}".format(index))
            return
        if not self._MATRIX_BUTTON_4_4_DOWN(index):
            logger.warning("button signal not process success")

    def release_BTN(self, index):
        if index not in BUTTONS:
            logger.error("btn index error {}".format(index))
            return
        if deploy == "DEV":
            logger.info("DEV: release btn {}".format(index))
            return
        self.BTNState[index] = 0

    def sendPS2(self, byte):
        print("send " + byte)

    # #Temporary code for sending a ps/2 scan code via uart
    # def send_ps2_keydown(self, code):
    #     if not self.ps2_uart_port:
    #         return
    #     if code in SCANCODE_KEYDOWN:
    #         self.ps2_uart_port.write(SCANCODE_KEYDOWN[code])
    #
    # def send_ps2_keyup(self, code):
    #     if not self.ps2_uart_port:
    #         return
    #     if code in SCANCODE_KEYUP:
    #         self.ps2_uart_port.write(SCANCODE_KEYUP[code])


    def programBit(self):
        if deploy == "DEV":
            print("program Bit, path: " + bitFilePath)
            return
        fpga.program_file(bitFilePath)


    def getSEG(self):
        for i in range(0, 8):
            self.SEGState[i] = (self.SEGState[i] + random.randint(0, 8)) % 8
        return self.SEGState

    def getLED(self):
        for i in range(0, 16):
            self.LEDState[i] = (self.LEDState[i] + random.randint(0, 16)) % 2
        return self.LEDState

    def get_4SEG_1LED(self):
        data = self._READ_4SEG_1LED()
        for i in range(0, 16):
            if i&1 :
                index = ((data['seg'][i-1]&15)<<4) | (data['seg'][i]&15)
                logger.error("index: " + str(data['seg'][i-1]) + " " + str(data['seg'][i]) + " " + str(index))
                self.SEGState[i>>1] = index
                # self.SEGState[i>>1] = random.randint(0, 8) % 8
            self.LEDState[i] = data['led'][i]
            # self.LEDState[i] = random.randint(0, 16) % 2
        return {'seg': self.SEGState, 'led': self.LEDState}


    def _WRITE_SN74HC595(self):
        for s in self.SWState:  # 4.5v工作电压下，最多支持25MHz；2v工作电压下，最多支持5MHz
            write(CLK_595, 0)
            write(SER_595, s)  # 串行输出16个SW状态
            write(CLK_595, 1)
        write(CLK_595, 0)
        write(CLK_595, 1)

    def _MATRIX_BUTTON_4_4_DOWN(self, id):
        flag = False

        row = id // 4
        col = id % 4

        write(BUTTONS_OUT[2], 0)  # button signal is start by 0
        write(BUTTONS_OUT[2], 1)

        time.sleep(0.15)  # delay time for flutter-free, duration need to be reconsider

        for i in range(50):
            rCol0 = read(BUTTONS_IN[0])
            rCol1 = read(BUTTONS_IN[1])
            rCol2 = read(BUTTONS_IN[2])
            rCol3 = read(BUTTONS_IN[3])
            # print("{} --> pin {} {} {} {}\t: val {} {} {} {}".
            #            format(i, BUTTONS_IN[0], BUTTONS_IN[1], BUTTONS_IN[2], BUTTONS_IN[3],
            #                   rCol0, rCol1, rCol2, rCol3))
            if row == 0 and rCol3 == 1 and rCol2 == 1 and rCol1 == 1 and rCol0 == 0:
                # logger.info("0 1110")
                write(BUTTONS_OUT[col], 0)
                self.BTNState[id] = 1
                flag = True
                break
            if row == 1 and rCol3 == 1 and rCol2 == 1 and rCol1 == 0 and rCol0 == 1:
                # logger.info("1 1101")
                write(BUTTONS_OUT[col], 0)
                self.BTNState[id] = 1
                flag = True
                break
            if row == 2 and rCol3 == 1 and rCol2 == 0 and rCol1 == 1 and rCol0 == 1:
                # logger.info("2 1011")
                write(BUTTONS_OUT[col], 0)
                self.BTNState[id] = 1
                flag = True
                break
            if row == 3 and rCol3 == 0 and rCol2 == 1 and rCol1 == 1 and rCol0 == 1:
                # logger.info("3 0111")
                write(BUTTONS_OUT[col], 0)
                self.BTNState[id] = 1
                flag = True
                break
            time.sleep(0.003)

        time.sleep(0.1)  # delay time for fpga to get the col signal while specific row
        # but the time can't be too long, prevent an unexpected new 'start'
        write(BUTTONS_OUT[col], 1)
        self.BTNState[id] = 0
        return flag

    def _READ_4SEG_1LED(self):
        seg = []
        led = []
        write(SEGLED_CLK, 1)
        time.sleep(0.005)
        write(SEGLED_CLK, 0)
        time.sleep(0.005)
        for i in range(0, 16):
            write(SEGLED_CLK, 1)
            time.sleep(0.005)

            tmp = 0
            for j in range(0, 4):
                tmp = (tmp<<1) | read(SEGLED_DATA[j])
            logger.error(tmp)
            # seg.append(tmp % 16)
            seg.append(tmp)
            # led.append(read(SEGLED_DATA[4]) % 2)
            led.append(read(SEGLED_DATA[4]))

            write(SEGLED_CLK, 0)
            time.sleep(0.005)

        write(SEGLED_CLK, 0)
        return {'seg': seg, 'led': led}


def write(pin, val):
    if deploy == 'DEV':
        logger.debug('Function "rpi.write()" called with pin={}, val={} '
                     'in development mode.'.format(pin, val))
        return
    logger.info('rpi write ' + str(val) + ' to pin ' + str(pin))
    wiringpi.digitalWrite(pin, val)

def read(pin):
    if deploy == 'DEV':
        logger.debug('Function "rpi.read()" called with pin={} '
                     'in development mode.'.format(pin))
        return
    return wiringpi.digitalRead(pin)

rpi = RPI()
