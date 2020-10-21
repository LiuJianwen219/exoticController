# -*- coding: utf-8 -*-
import importlib
import logging
import subprocess as sp

import device
from config import deploy, platform
from util import util

logger = logging.getLogger('rpi.' + __name__)

try:
    if deploy == 'DEV':
        platformC = importlib.import_module('.mock', 'device')
    else:
        platformC = importlib.import_module('.' + platform, 'device')
except ImportError:
    logger.error('Failed to find corresponding FPGA module named'
                 '{}.py'.format(platform), exc_info=True)
    util.exit(1)


def check_alive():
    platformC.check_alive()


def program_file(file_path):
    return platformC.program_file(file_path)


def program_idle():
    logger.info("--> program_idel() <--")
    return platformC.program_file('ext/' + platform + '.bit')


def check_djtgcfg():
    if deploy == 'DEV':
        logger.debug('Function "fpga.check_djtgcfg()" called in development mode.')
        return

    try:
        res = sp.check_output('djtgcfg', shell=True)
    except sp.CalledProcessError as e:
        res = e.output

    if not res.startswith(b'ERROR: no command specified'):
        logger.error('The output of command "djtgcfg" is unexpected. '
                     'Please check whether it is correctly installed.')
        util.exit(1)


def init():
    check_djtgcfg()
    check_alive()
    logger.info('Successfully connected to the FPGA board.')
