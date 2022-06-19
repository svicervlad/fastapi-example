from loguru import logger

def configure_logger():
    '''
    Configure logger
    '''
    logger.add("file.log", rotation="5 MB")
