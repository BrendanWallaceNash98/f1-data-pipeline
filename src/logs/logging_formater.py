import logging
import os
from logging.handlers import TimedRotatingFileHandler


def generate_logger(name: str) -> logging.Logger:
    formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)
    log_name = f'src/logs/{name}/{name}.log'
    os.makedirs(os.path.dirname(log_name), exist_ok=True)
    handler = TimedRotatingFileHandler(log_name, when='D', interval=1)
    handler.suffix = "%Y-%m-%d"
    handler.formatter = formater
    logger.addHandler(handler)
    return logger