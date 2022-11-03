import logging

from global_settings import state_project


def get_logger(module_name: str):

    FORMAT = '%(asctime)s - %(filename)s - %(levelname)s - %(message)s - %(lineno)d'

    if state_project():
        logging.basicConfig(format=FORMAT, filename="logfile.log")
    else:
        logging.basicConfig(format=FORMAT)

    logger = logging.getLogger(module_name)

    return logger