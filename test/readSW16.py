import logging
import wiringpi

from config import deploy

logger = logging.getLogger('rpi.' + __name__)

SW_INPUTS = []

def read(pin):
    if deploy == 'DEV':
        logger.debug('Function "rpi.read()" called with pin={} '
                     'in development mode.'.format(pin))
        return
    return wiringpi.digitalRead(pin)

def main():
    for pin in SW_INPUTS:
        wiringpi.pinMode(pin, wiringpi.INPUT)
        wiringpi.pullUpDnControl(pin, wiringpi.PUD_UP)
    old_pins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    while True:
        flag = False
        read_pins = []
        for i in range(16):
            read_pins.append(read(SW_INPUTS[i]))
        for i in range(16):
            if old_pins[i] != read_pins[i]:
                flag = True
                break
        if flag == True:
            logger.info("{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}",
                        read_pins[0], read_pins[1], read_pins[2], read_pins[3],
                        read_pins[4], read_pins[5], read_pins[6], read_pins[7],
                        read_pins[8], read_pins[9], read_pins[10], read_pins[11],
                        read_pins[12], read_pins[13], read_pins[14], read_pins[15])
            old_pins.clear()
            for i in range(16):
                old_pins.append(read_pins[i])

if __name__ == '__main__':
    main()
