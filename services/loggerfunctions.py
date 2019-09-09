import logging


def create_logger(name):
    log = logging.getLogger(name)
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
    log.setLevel(logging.DEBUG)
    log.addHandler(log_handler)
    return log
