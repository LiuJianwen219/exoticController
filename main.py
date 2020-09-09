# -*- coding:utf-8 -*-
import json
import time

import websocket
from config import *
from module.network import on_message, on_error, on_close, on_open
from module.rpi import state
from util.contants import *

try:
    import thread
except ImportError:
    import _thread as thread

from threading import Timer

def sendBeat():
    data = {
        'type': UPDATE_DEVICE,
        'index': deviceNum,
        'time': time.time(),
        # "time" : time.strftime("%Y-%m-%d %b %a %H:%M:%S", time.localtime()),
        'state': state,
    }
    ws.send(json.dumps(data).encode("utf-8"))
    # Timer(1, sendBeat).start()

if __name__ == "__main__":
    websocket.enableTrace(True)
    print(host)
    print(port)
    ws = websocket.WebSocketApp("ws://" + "localhost" + ":" + "20200",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    Timer(1, sendBeat).start()

    ws.run_forever()
    print("never here")
