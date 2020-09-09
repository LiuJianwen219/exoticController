# -*- coding: utf-8 -*-
import logging
import re
import subprocess as sp

from util import util

logger = logging.getLogger('rpi.' + __name__)

params = {
    'CABLE_NAME': 'JtagHs2',
    'FPGA_NUMBER': 'XC7K160T'
}

# check the .bit file exist
def _validate_file(file_path):
    res = sp.check_output('file {}'.format(file_path), shell=True)
    # TODO

# check the download cable and the fpga exist
def _query_index():
    try:
        cmd = 'djtgcfg enum | grep "Device: {CABLE_NAME}"'.format(**params)
        res = sp.check_output(cmd, shell=True)
        if len(res) < 1:
            msg = 'Failed to detect download cable "{CABLE_NAME}".'.format(**params)
            logger.error(msg)
            util.exit(1)

        cmd = 'djtgcfg init -d {CABLE_NAME} | grep {FPGA_NUMBER}'.format(**params)
        res = sp.check_output(cmd, shell=True)
        if len(res) < 1:
            msg = 'Failed to detect FPGA device {FPGA_NUMBER}.'.format(**params)
            logger.error(msg)
            util.exit(1)
    except Exception as e:
        logger.error('Error connecting to FPGA board', exc_info=True)
        util.exit(1)

    regex = r'\s*Device (\d+): {FPGA_NUMBER}'.format(**params)
    index = re.match(regex, res.decode('utf-8')).groups()[0]
    return index

# available for out to check
def check_alive():
    _query_index()

# available for out tho download .bit
def program_file(file_path):
    index = _query_index()
    _validate_file(file_path)
    try:
        cmd = ('djtgcfg prog -d {} --index {} --file {} | grep "Programming '
               'succeeded."').format(params['CABLE_NAME'], index, file_path)
        res = sp.check_output(cmd, shell=True)
        if len(res) < 1:
            logger.error('Unexpected error occurs during programming the FPGA board.')
            return False
        else:
            logger.info('Programming {} to FPGA succeeded!'.format(file_path))
            return True
    except Exception as e:
        logger.error('Error programming FPGA board.', exc_info=True)
        return False
