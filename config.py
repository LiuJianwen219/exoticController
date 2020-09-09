import configparser
import logging.config
import yaml
import os


# log configuration
log_conf_file = os.path.join(os.getcwd(), 'logger.yaml')
if os.path.exists(log_conf_file):
    with open(log_conf_file, 'rt') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


settings_file = os.path.join(os.getcwd(), 'settings.ini')
if os.path.exists(settings_file):
    config = configparser.ConfigParser()
    config.read(settings_file)

    host = config["WEB_SERVER"]["HOST"]
    port = config["WEB_SERVER"]["PORT"]
    deviceNum = config["RPI_CLIENT"]["DEVICE_NUM"]
    bitFilePath = config["RPI_CLIENT"]["BIT_FILE_PATH"]
else:
    exit(-1)


# test configurations
if __name__ == '__main__':
    logger = logging.getLogger('exotic')
    logger.error("check program path")
