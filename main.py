import sys
from src.logging.logger import logging
from src.exception.exception import CustomException

if __name__ == "__main__":
    try:
        logging.info("Testing logging and custom exception")
        print(1 / 0)  # Intentional error
    except Exception as e:
        logging.error("An exception occurred")
        raise CustomException(e, sys) # type: ignore
