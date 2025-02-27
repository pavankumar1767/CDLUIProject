import logging
import os


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("test.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()