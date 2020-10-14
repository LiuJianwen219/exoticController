# -*- coding:utf-8 -*-
from module.network import websocketServerStart
from module.rpi import rpi
from module import fpga
from util import util

try:
    import thread
except ImportError:
    import _thread as thread

if __name__ == "__main__":
    util.setup_trap()
    rpi.init()
    fpga.init()
    websocketServerStart()
    print("never here")
