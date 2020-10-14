import wiringpi
import time
import logging

logger = logging.getLogger("rpi")

RPI_INPUTS = [4, 5, 6, 7]
RPI_OUTPUTS = [21, 22, 23, 24, 25, 0, 1, 2, 3]

SER = 21
OE = 22
RCLK = 23
SRCLK = 24
SRCLR = 25

def init():
    wiringpi.wiringPiSetup()
    for pin in RPI_INPUTS:
        wiringpi.pinMode(pin, wiringpi.INPUT)
        wiringpi.pullUpDnControl(pin, wiringpi.PUD_UP)
    for pin in RPI_OUTPUTS:
        wiringpi.pinMode(pin, wiringpi.OUTPUT)
        wiringpi.digitalWrite(pin, 1)
#    wiringpi.setPadDrive(0, 7)
    logger.info('GPIO ports initialization done.')

def write(pin, val):
    logger.info('rpi write ' + str(val) + ' to pin ' + str(pin))
    wiringpi.digitalWrite(pin, val)

def read(pin):
    return wiringpi.digitalRead(pin)

def _WRITE_SN74HC595(SWState):
    for s in SWState:  # 4.5v工作电压下，最多支持25MHz；2v工作电压下，最多支持5MHz
        write(SRCLK, 0)
        write(RCLK, 0)
        write(SER, s)  # 串行输出16个SW状态
        write(RCLK, 1)
        write(SRCLK, 1)
    write(RCLK, 0)
    write(RCLK, 1)

def _INIT_SN74HC595():
    write(SRCLR, 1)
    write(OE,0)

BUTTONS_OUT = [0, 1, 2, 3]
BUTTONS_IN = [4, 5, 6, 7]
BTNState = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def _INIT_BUTTON_4_4_DOWN():
    write(BUTTONS_OUT[0], 1)
    write(BUTTONS_OUT[1], 1)
    write(BUTTONS_OUT[2], 1)
    write(BUTTONS_OUT[3], 1)

def _MATRIX_BUTTON_4_4_DOWN(id):
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
        #print("{} --> pin {} {} {} {}\t: val {} {} {} {}".
        #            format(i, BUTTONS_IN[0], BUTTONS_IN[1], BUTTONS_IN[2], BUTTONS_IN[3],
        #                   rCol0, rCol1, rCol2, rCol3))
        if row == 0 and rCol3 == 1 and rCol2 == 1 and rCol1 == 1 and rCol0 == 0:
            #logger.info("0 1110")
            write(BUTTONS_OUT[col], 0)
            BTNState[id] = 1
            flag = True
            break
        if row == 1 and rCol3 == 1 and rCol2 == 1 and rCol1 == 0 and rCol0 == 1:
            #logger.info("1 1101")
            write(BUTTONS_OUT[col], 0)
            BTNState[id] = 1
            flag = True
            break
        if row == 2 and rCol3 == 1 and rCol2 == 0 and rCol1 == 1 and rCol0 == 1:
            #logger.info("2 1011")
            write(BUTTONS_OUT[col], 0)
            BTNState[id] = 1
            flag = True
            break
        if row == 3 and rCol3 == 0 and rCol2 == 1 and rCol1 == 1 and rCol0 == 1:
            #logger.info("3 0111")
            write(BUTTONS_OUT[col], 0)
            BTNState[id] = 1
            flag = True
            break
        time.sleep(0.003)

    time.sleep(0.1)  # delay time for fpga to get the col signal while specific row
                        # but the time can't be too long, prevent an unexpected new 'start'
    write(BUTTONS_OUT[col], 1)
    BTNState[id] = 0
    return flag



if __name__ == '__main__':
    time.sleep(1)
    init()

    _INIT_SN74HC595()
    t = [0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1]
    _WRITE_SN74HC595(t)

    _INIT_BUTTON_4_4_DOWN()
    for i in range(16):
        _MATRIX_BUTTON_4_4_DOWN(i)
        #time.sleep(0.5)


    exit(0)








