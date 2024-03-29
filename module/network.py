# -*- coding:utf-8 -*-
import datetime
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

# Get video information
import ctypes
import inspect
import threading
import subprocess as sp

state = 0
fps = 25
width = 960
height = 540

p1cmd = ['raspivid', '-t', '0', '-w', '960', '-h', '540', '-fps', '25', '-b', '200000', '-vf', '-hf', '-o', '-']
p2cmd = ['ffmpeg', '-i', '-', '-vcodec', 'copy', '-bufsize', '2k', '-b:v', '2k', '-probesize', '32', '-an', '-r', '25',
         '-f', 'flv', 'rtmp://47.96.95.218/live/device' + str(deviceNum)]
# raspivid -t 0 -w 960 -h 540 -fps 25 -b 200000 -vf -hf -o -
# ffmpeg -i - -vcodec cop -bufsize 2k -b:v 2k -probesize 32 -an -r 25 -f flv rtmp://47.96.95.218/live/device0
cmdList = []
cmdList.append(p2cmd)
cmdList.append(p1cmd)
global p1, p2

debugx = False


def push():
    global p1, p2
    p1.stdout.flush()
    while True:
        line = p1.stdout.readline()
        if not line:
            break
        p2.stdin.write(line)


##---------------------------------------------------------

def on_message(ws, message):
    if debugx:
        print(message)
    dict_ = json.loads(message)
    global p1, p2
    if dict_["type"] == UPDATE_DEVICE_SUCC:
        #print("UPDATE_DEVICE_SUCC")
        pass
    elif dict_['type'] == ACQUIRE_DEVICE_FOR_EXP:
        print("exp   exp    exp")
        print(dict_['content']['Uid'])
        rpi.setStateBusy()

        data = {'type': ACQUIRE_DEVICE_SUCC_EXP,
                'content': {
                    'device': deviceNum,
                    'Uid': dict_['content']['Uid'],
                    'device_tags': DEVICE_TAGS,
                    'time': time_now(),
                }}
        ws.send(json.dumps(data).encode("utf-8"))

        # start subprocess
        p1 = sp.Popen(p1cmd, stdout=sp.PIPE, stderr=open(os.devnull, 'wb'))
        p2 = sp.Popen(p2cmd, stdin=sp.PIPE)
        # open a new thread to write to the pipe
        threadpush = threading.Thread(target=push)
        threadpush.setDaemon(True)
        threadpush.setName("pushing_stream_thread")
        threadpush.start()
    elif dict_['type'] == ACQUIRE_DEVICE_FOR_TEST:
        print("test  test  test")
        print(dict_['content']['Uid'])
        rpi.setStateBusy()
        data = {'type': ACQUIRE_DEVICE_SUCC_TEST,
                'content': {
                    'device': deviceNum,
                    'Uid': dict_['content']['Uid'],
                    'device_tags': DEVICE_TAGS,
                    'time': time_now(),
                }}
        ws.send(json.dumps(data).encode("utf-8"))

    elif dict_['type'] == ACT_SYNC_SW_BTN:
        data = {'type': ACT_SYNC_SW_BTN_SUCC,
                'content': {
                    'SWState': rpi.SWState,
                    'BTNState': rpi.BTNState,
                    'time': time_now(),
                }}
        ws.send(json.dumps(data).encode("utf-8"))
    elif dict_['type'] == ACT_RELEASE:
        rpi.setStateFree()
        # stop the sub process
        p1.kill()
        p2.kill()

    elif dict_['type'] == OP_SW_OPEN_DEVICE:
        rpi.open_SW(dict_['content']['id'])

        data = {'type': OP_SW_CHANGED,
                'content': {
                    'id': dict_['content']['id'],
                    'changeTo': dict_['content']['changeTo'],
                    'time': time_now(),
                }}
        ws.send(json.dumps(data).encode("utf-8"))
    elif dict_['type'] == OP_SW_CLOSE_DEVICE:
        rpi.close_SW(dict_['content']['id'])

        data = {'type': OP_SW_CHANGED,
                'content': {
                    'id': dict_['content']['id'],
                    'changeTo': dict_['content']['changeTo'],
                    'time': time_now(),
                }}
        ws.send(json.dumps(data).encode("utf-8"))
    elif dict_['type'] == OP_BTN_PRESS_DEVICE:
        rpi.press_BTN(dict_['content']['id'])

        data = {'type': OP_BTN_CHANGED,
                'content': {
                    'id': dict_['content']['id'],
                    'changeTo': dict_['content']['changeTo'],
                    'time': time_now(),
                }}
        ws.send(json.dumps(data).encode("utf-8"))
    elif dict_['type'] == OP_BTN_RELEASE_DEVICE:
        rpi.release_BTN(dict_['content']['id'])

        data = {'type': OP_BTN_CHANGED,
                'content': {
                    'id': dict_['content']['id'],
                    'changeTo': dict_['content']['changeTo'],
                    'time': time_now(),
                }}
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
        print(dict_['content']['compileId'])
        userId = dict_['content']['userId']
        type = dict_['content']['type']
        expId = dict_['content']['expId']
        isUpload = dict_['content']['isUpload']
        compileId = dict_['content']['compileId']
        bitFileName = dict_['content']['bitFileName']

        if not isUpload or isUpload == "false":
            url = "http://" + FILE_SERVER_IP + ":" + FILE_SERVER_PORT + "/" + GET_ONLINE_BIT_API
            values = {
                "deviceId": str(deviceNum),
                "userId": userId,
                "experimentType": type,
                "experimentId": expId,
                "compileId": compileId,
            }
            r = requests.get(url, params=values)  # create HTTP response object
        else:
            url = "http://" + FILE_SERVER_IP + ":" + FILE_SERVER_PORT + "/" + GET_OWN_BIT_API
            values = {
                "deviceId": str(deviceNum),
                "userId": userId,
                "experimentType": type,
                "experimentId": expId,
                "bitFileName": bitFileName,
            }
            r = requests.get(url, params=values)  # create HTTP response object

        if r.status_code == 200:
            print(bitFilePath)
            if os.path.exists(bitFilePath):
                print(os.getcwd())
            with open(bitFilePath, 'wb') as f:
                f.write(r.content)

            rpi.programBit()  # program the constant filepath

            data = {'type': OP_PROGRAM_SUCC,
                    'content': {
                        'time': time_now(),
                    }}
            ws.send(json.dumps(data).encode("utf-8"))
        else:
            data = {'type': OP_PROGRAM_ERROR,
                    'content': {
                        'time': time_now(),
                    }}
            ws.send(json.dumps(data).encode("utf-8"))

    elif dict_['type'] == REQ_SEG:
        seg = rpi.getSEG()
        data = {'type': REQ_SEG_SUCC, 'seg': seg}
        ws.send(json.dumps(data).encode("utf-8"))
    elif dict_['type'] == REQ_LED:
        led = rpi.getLED()
        data = {'type': REQ_LED_SUCC, 'led': led}
        ws.send(json.dumps(data).encode("utf-8"))
    elif dict_['type'] == REQ_READ_DATA:
        seg_led = rpi.get_4SEG_1LED()
        data = {'type': REQ_READ_DATA_SUCC, 'seg': seg_led['seg'], 'led': seg_led['led']}
        ws.send(json.dumps(data).encode("utf-8"))

    elif dict_['type'] == TEST_PROGRAM:
        # --------------------------------------------------
        # --------------------------------------------------
        # -------------TODO---------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # "userId": request.POST.get("userId", None),
        # "testId": request.POST.get("testId", None),
        # "submitId": request.POST.get("submitId", None),
        # "topic": request.POST.get("topic", None),
        # "state": request.POST.get("state", None),
        # "status": request.POST.get("status", None),
        # "message": request.POST.get("message", None),
        print(dict_['content']['userId'])
        print(dict_['content']['testId'])
        print(dict_['content']['submitId'])
        print(dict_['content']['topic'])

        userId = dict_['content']['userId']
        testId = dict_['content']['testId']
        submitId = dict_['content']['submitId']
        topic = dict_['content']['topic']

        values = {
            "userId": userId,
            "testId": testId,
            "submitId": submitId,
            "topic": topic,
        }

        url = "http://" + FILE_SERVER_IP + ":" + FILE_SERVER_PORT + "/" + GET_BIT_API
        print(url)
        print(values)
        r = requests.get(url=url, params=values)  # create HTTP response object

        # --------------------------------------------------

        if r.status_code == 200:
            print(bitFilePath)
            if os.path.exists(bitFilePath):
                print(os.getcwd())
            with open(bitFilePath, 'wb') as f:
                f.write(r.content)

            print(userId, testId, submitId, topic, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            start = time.time()
            rpi.programBit()  # program the constant filepath
            end = time.time()
            print(userId, testId, submitId, topic, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print(userId, testId, submitId, topic, end-start)

            data = {'type': TEST_PROGRAM_SUCC,
                    'content': {
                        'time': time_now(),
                    }}
            ws.send(json.dumps(data).encode("utf-8"))
        else:
            print(r.content)
            data = {'type': TEST_PROGRAM_FAIL,
                    'content': {
                        'time': time_now(),
                    }}
            ws.send(json.dumps(data).encode("utf-8"))
    elif dict_['type'] == TEST_READ_RESULT:
        testSummary, cycle, testResult = rpi.readTestResult()
        data = {'type': TEST_READ_RESULT_SUCC,
                'testStatus': "Complete",
                'testResult': testResult,
                'testSummary': "测试通过" if testSummary == 15 else "测试失败",
                'usingCycle': cycle,
                'info': "测试超时" if testSummary == -1 else "测试正常",
                'time': time_now(),
                }
        ws.send(json.dumps(data).encode("utf-8"))

    elif dict_['type'] == INIT_FILE_UPLOAD:
        data = {'type': INIT_FILE_UPLOAD_SUCC,
                'content': {
                    'time': time_now(),
                }}
        ws.send(json.dumps(data).encode("utf-8"))


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    time.sleep(2)
    data = {
        'type': AUTH_DEVICE,
        'index': deviceNum,
        'device_tags': DEVICE_TAGS,
        'time': time_now(),
    }
    ws.send(json.dumps(data))

    time.sleep(1)
    data = {
        'type': UPDATE_DEVICE,
        'index': deviceNum,
        'time': time_now(),
        'state': rpi.getRPIState(),
        'device_tags': DEVICE_TAGS,
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
            'time': time_now(),
            'state': rpi.getRPIState(),
            'device_tags': DEVICE_TAGS,
        }
        ws.send(json.dumps(data).encode("utf-8"))
        Timer(30, sendBeat).start()

    Timer(30, sendBeat).start()

    ws.run_forever()


def time_now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
