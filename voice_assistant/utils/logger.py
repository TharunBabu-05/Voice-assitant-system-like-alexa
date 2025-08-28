import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('voice_assistant')

def log_info(msg):
    logger.info(msg)

def log_error(msg):
    logger.error(msg)
