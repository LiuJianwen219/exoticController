# -*- coding:utf-8 -*-
import json
import os
import time

import requests
import websocket
from threading import Timer

from config import *
from module.rpi import rpi

from util.contants import *

logger = logging.getLogger('rpi.' + __name__)

def on_message(ws, message):
    print(message)
    dict_ = json.loads(message)
    if dict_["type"] == UPDATE_DEVICE_SUCC:
        print("UPDATE_DEVICE_SUCC")
    elif dict_['type'] == ACQUIRE_DEVICE_FOR_EXP:
        print(dict_['content']['Uid'])
        global state
        state = 1
        data = {'type': ACQUIRE_DEVICE_SUCC_EXP,
                'content': {'device': deviceNum, 'Uid': dict_['content']['Uid']}}
        ws.send(json.dumps(data).encode("utf-8"))
    elif dict_['type'] == ACT_SYNC_SW_BTN:
        data = {'type': ACT_SYNC_SW_BTN_SUCC,
                'content': {'SWState': rpi.SWState, 'BTNState': rpi.BTNState}}
        ws.send(json.dumps(data).encode("utf-8"))
    elif dict_['type'] == ACT_RELEASE:
        state = 0
    elif dict_['type'] == OP_SW_OPEN_DEVICE:
        rpi.open_SW(dict_['content']['id'])

        data = {'type': OP_SW_CHANGED,
                'content': {'id': dict_['content']['id'],
                            'changeTo': dict_['content']['changeTo']}}
        ws.send(json.dumps(data).encode("utf-8"))
    elif dict_['type'] == OP_SW_CLOSE_DEVICE:
        rpi.close_SW(dict_['content']['id'])

        data = {'type': OP_SW_CHANGED,
                'content': {'id': dict_['content']['id'],
                            'changeTo': dict_['content']['changeTo']}}
        ws.send(json.dumps(data).encode("utf-8"))
    elif dict_['type'] == OP_BTN_PRESS_DEVICE:
        rpi.press_BTN(dict_['content']['id'])

        data = {'type': OP_BTN_CHANGED,
                'content': {'id': dict_['content']['id'],
                            'changeTo': dict_['content']['changeTo']}}
        ws.send(json.dumps(data).encode("utf-8"))
    elif dict_['type'] == OP_BTN_RELEASE_DEVICE:
        rpi.release_BTN(dict_['content']['id'])

        data = {'type': OP_BTN_CHANGED,
                'content': {'id': dict_['content']['id'],
                            'changeTo': dict_['content']['changeTo']}}
        ws.send(json.dumps(data).encode("utf-8"))
    elif dict_['type'] == OP_PS2_SEND:

        rpi.sendPS2(dict_['content']['byte'])

        data = {'type': OP_PS2_SEND_SUCC}
        ws.send(json.dumps(data).encode("utf-8"))

    elif dict_['type'] == OP_PROGRAM:
        print(dict_['content']['userId'])
        print(dict_['content']['type'])
        print(dict_['content']['expId'])
        print(dict_['content']['isUpload'])
        print(dict_['content']['bitFileName'])
        userId = dict_['content']['userId']
        type = dict_['content']['type']
        expId = dict_['content']['expId']
        isUpload = dict_['content']['isUpload']
        bitFileName = dict_['content']['bitFileName']

        url = "http://"+webIP+":"+webPort+"/experiment/download/?deviceId=" + \
              str(deviceNum) + "&userId=" + userId + "&type=" + type + "&expId=" + \
              expId + "&isUpload=" + str(isUpload) + "&bitFileName=" + bitFileName
        r = requests.get(url)  # create HTTP response object

        if r.status_code == 200:
            print(bitFilePath)
            if os.path.exists(bitFilePath):
                print(os.getcwd())
            with open(bitFilePath, 'wb') as f:
                f.write(r.content)

            rpi.programBit() # program the constant filepath

            data = {'type': OP_PROGRAM_SUCC}
            ws.send(json.dumps(data).encode("utf-8"))
        else:
            data = {'type': OP_PROGRAM_ERROR}
            ws.send(json.dumps(data).encode("utf-8"))

    elif dict_['type'] == REQ_SEG:
        seg = rpi.getSEG()
        data = {'type': REQ_SEG_SUCC, 'seg': seg}
        ws.send(json.dumps(data).encode("utf-8"))

    elif dict_['type'] == REQ_LED:
        led = rpi.getLED()
        data = {'type': REQ_LED_SUCC, 'led': led}
        ws.send(json.dumps(data).encode("utf-8"))

    elif dict_['type'] == INIT_FILE_UPLOAD:
        data = {'type': INIT_FILE_UPLOAD_SUCC}
        ws.send(json.dumps(data).encode("utf-8"))

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    data = {
        'type': AUTH_DEVICE,
        'index': deviceNum,
    }
    ws.send(json.dumps(data))

    data = {
        'type': UPDATE_DEVICE,
        'index': deviceNum,
        'time': time.time(),
        # "time" : time.strftime("%Y-%m-%d %b %a %H:%M:%S", time.localtime()),
        'state': rpi.state,
    }
    ws.send(json.dumps(data).encode("utf-8"))



def websocketServerStart():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://" + host + ":" + port,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    def sendBeat():
        data = {
            'type': UPDATE_DEVICE,
            'index': deviceNum,
            'time': time.time(), # "time" : time.strftime("%Y-%m-%d %b %a %H:%M:%S", time.localtime()),
            'state': rpi.state,
        }
        ws.send(json.dumps(data).encode("utf-8"))
        # Timer(1, sendBeat).start()

    Timer(1, sendBeat).start()

    ws.run_forever()