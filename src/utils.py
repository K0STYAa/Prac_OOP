import datetime
import logging
from pathlib import Path

HOURS_PER_DAY = 24

def get_logger():
    logs_path = Path('./logs')
    logs_path.mkdir(exist_ok=True)
    logging.basicConfig(
        filemode='w',
        format='[%(levelname)s] %(message)s',
        filename=logs_path / f'{datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.txt',
        level=logging.DEBUG,
        encoding='utf-8',
    )
    logger = logging.getLogger(__name__)

    return logger

logger = get_logger()