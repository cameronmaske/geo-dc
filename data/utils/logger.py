import logging

def get_logger():
    """
    A default logging level.
    """
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)
