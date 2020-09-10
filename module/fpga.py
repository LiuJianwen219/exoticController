# -*- coding: utf-8 -*-
import importlib
import logging
import subprocess as sp
from tornado.options import options

import device
from util import util

logger = logging.getLogger('rpi.' + __name__)

try:
    if options.deploy == 'DEV':
        platform = importlib.import_module('.mock', 'device')
    else:
        platform = importlib.import_module('.' + options.platform, 'device')
except ImportError:
    logger.error('Failed to find corresponding FPGA module named'
                 '{}.py'.format(options.platform), exc_info=True)
    util.exit(1)


def check_alive():
    platform.check_alive()


def program_file(file_path):
    return platform.program_file(file_path)


def program_idle():
    return platform.program_file('ext/' + options.platform + '.bit')


def check_djtgcfg():
    if options.deploy == 'DEV':
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
