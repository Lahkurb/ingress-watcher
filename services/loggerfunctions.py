import logging


def create_logger(name):
    """
    Create a logger with a program specific formatting

    :param name: name of the logger
    :return:
    """
    log = logging.getLogger(name)
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s"))
    log.setLevel(logging.DEBUG)
    log.addHandler(log_handler)
    return log
