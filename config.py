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

    webIP = config["WEB_SERVER"]["WEBIP"]
    webPort = config["WEB_SERVER"]["WEBPORT"]
    host = config["WEB_SERVER"]["HOST"]
    port = config["WEB_SERVER"]["PORT"]
    deploy = config["RPI_CLIENT"]["DEPLOY"]
    deviceNum = config["RPI_CLIENT"]["DEVICE_NUM"]
    bitFilePath = os.path.join(os.getcwd(), config["RPI_CLIENT"]["BIT_FILE_PATH"])
    platform = config["RPI_CLIENT"]["PLATFORM"]
    FILE_SERVER_IP = config["FILE_SERVER"]["FILE_SERVER_IP"]
    FILE_SERVER_PORT = config["FILE_SERVER"]["FILE_SERVER_PORT"]
    GET_BIT_API = config["FILE_SERVER"]["GET_BIT_API"]
    GET_ONLINE_BIT_API = config["FILE_SERVER"]["GET_ONLINE_BIT_API"]
    GET_OWN_BIT_API = config["FILE_SERVER"]["GET_OWN_BIT_API"]
    MAX_TIME = config["TEST_PARAM"]["MAX_TIME"]
    print(webIP)
    print(webPort)
    print(host)
    print(port)
    print(deviceNum)
    print(bitFilePath)
else:
    exit(-1)


# test configurations
if __name__ == '__main__':
    logger = logging.getLogger('exotic')
    logger.error("check program path")
