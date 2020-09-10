# -*- coding:utf-8 -*-
from module.network import websocketServerStart
from util import util

try:
    import thread
except ImportError:
    import _thread as thread



if __name__ == "__main__":
    util.setup_trap()
    websocketServerStart()
    print("never here")
