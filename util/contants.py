# # Communication protocol
# types = [
#     'ACT_ACQUIRE', #
#     'ACT_RELEASE',
#     'ACT_BROADCAST',
#     'ACT_AUTH',
#     'ACT_SYNC', #
#     'ACT_CHANGE_MODE',
#     'STAT_AUTH_SUCC',
#     'STAT_AUTH_FAIL',
#     'STAT_INPUT',
#     'STAT_OUTPUT',
#     'STAT_UPLOADED',
#     'STAT_DOWNLOADED',
#     'STAT_PROGRAMMED',
#     'STAT_DOWNLOAD_FAIL',
#     'OP_BTN_DOWN',
#     'OP_BTN_UP',
#     'OP_SW_OPEN',
#     'OP_SW_CLOSE',
#     'OP_PROG',
#     'INFO_USER_CHANGED',
#     'INFO_DISCONN',
#     'INFO_BROADCAST',
#     'INFO_MODE_CHANGED',
#     'INFO_VIDEO_URL',
#
#     'OP_PS2_KEYDOWN',
#     'OP_PS2_KEYUP',
#     'OP_INPUT_ON',
#     'OP_INPUT_OFF',
#     'OP_SERIAL_CONFIG',
#     'OP_SERIAL_TX',
#     'OP_SERIAL_RX',
#     'STAT_PROGRAM_FAIL',
# ]
#
# for i, type_ in enumerate(types):
#     exec('{} = {}'.format(type_, i))
#
# UPDATE_DEVICE = 100
# SYNC_DEVICE = 26
#

# Communication protocol
types = [
    'AUTH_USER',            # 0
    'AUTH_SUCC_USER',       # 1
    'AUTH_FAIL_USER',       # 2
    'AUTH_DEVICE',
    'AUTH_SUCC_DEVICE',
    'UPDATE_DEVICE',
    'UPDATE_DEVICE_SUCC',
    'ACT_SYNC',
    'SYNC_DEVICE',          # 8

    'ACT_ACQUIRE',
    'ACT_SYNC_SW_BTN',
    'ACT_SYNC_SW_BTN_SUCC',
    'INIT_FILE_UPLOAD',
    'INIT_FILE_UPLOAD_SUCC',    # 13
    'ACQUIRE_FAIL',
    'ACQUIRE_SUCC',
    'ACQUIRE_DEVICE_FOR_EXP',
    'ACQUIRE_DEVICE_SUCC_EXP',
    'ACQUIRE_DEVICE_FOR_TEST',  # 18
    'ACQUIRE_DEVICE_SUCC_TEST',

    'ACT_RELEASE',

    'REQ_SEG',
    'REQ_SEG_SUCC',
    'REQ_LED',
    'REQ_LED_SUCC', # 24
    'REQ_READ_DATA',
    'REQ_READ_DATA_SUCC',

    'OP_PROGRAM',
    'OP_PROGRAM_SUCC',

    'OP_SW_OPEN',       # 29
    'OP_SW_CLOSE',
    'OP_SW_OPEN_DEVICE',
    'OP_SW_CLOSE_DEVICE',
    'OP_SW_CHANGED',

    'OP_BTN_PRESS',     # 34
    'OP_BTN_RELEASE',
    'OP_BTN_PRESS_DEVICE',
    'OP_BTN_RELEASE_DEVICE',
    'OP_BTN_CHANGED',

    'OP_PS2_SEND',      # 39
    'OP_PS2_SEND_SUCC',

    'AUTH_RABBIT',
    'AUTH_RABBIT_SUCC',
    'AUTH_RABBIT_FAIL',

    'AUTH_RABBIT',      # 44
    'AUTH_RABBIT_SUCC',
    'AUTH_RABBIT_FAIL',
    'TEST_PROGRAM',
    'TEST_PROGRAM_SUCC',# 48
    'TEST_PROGRAM_FAIL',
    'TEST_READ_RESULT', # 50
    'TEST_READ_RESULT_SUCC',
]

for i, type_ in enumerate(types):
    exec('{} = {}'.format(type_, i))

SYS_DELAY = 100000000
# SYS_DELAY = 10
UPDATE_TIME = 3  # devices状态更新的周期，单位秒
