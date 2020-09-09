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
    'AUTH_USER',
    'AUTH_SUCC_USER',
    'AUTH_FAIL_USER',
    'AUTH_DEVICE',
    'AUTH_SUCC_DEVICE',
    'UPDATE_DEVICE',
    'UPDATE_DEVICE_SUCC',
    'ACT_SYNC',
    'SYNC_DEVICE',

    'ACT_ACQUIRE',
    'ACT_SYNC_SW_BTN',
    'ACT_SYNC_SW_BTN_SUCC',
    'INIT_FILE_UPLOAD',
    'INIT_FILE_UPLOAD_SUCC',
    'ACQUIRE_FAIL',
    'ACQUIRE_SUCC',
    'ACQUIRE_DEVICE_FOR_EXP',
    'ACQUIRE_DEVICE_SUCC_EXP',

    'ACT_RELEASE',

    'REQ_SEG',
    'REQ_SEG_SUCC',
    'REQ_LED',
    'REQ_LED_SUCC',

    'OP_PROGRAM',
    'OP_PROGRAM_SUCC',

    'OP_SW_OPEN',
    'OP_SW_CLOSE',
    'OP_SW_OPEN_DEVICE',
    'OP_SW_CLOSE_DEVICE',
    'OP_SW_CHANGED',

    'OP_BTN_PRESS',
    'OP_BTN_RELEASE',
    'OP_BTN_PRESS_DEVICE',
    'OP_BTN_RELEASE_DEVICE',
    'OP_BTN_CHANGED',

    'OP_PS2_SEND',
    'OP_PS2_SEND_SUCC',
]

for i, type_ in enumerate(types):
    exec('{} = {}'.format(type_, i))

SYS_DELAY = 100000000
# SYS_DELAY = 10
UPDATE_TIME = 3  # devices状态更新的周期，单位秒