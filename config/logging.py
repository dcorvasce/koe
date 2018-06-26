'''Initialize logger for the entire application'''
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s --: %(message)s')

file_handler = logging.FileHandler('/tmp/koe.log')
file_handler.setFormatter(log_formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
