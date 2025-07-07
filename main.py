# main.py

import sys
from src.components.data_ingestion import DataIngestion
from src.entity.entity_config import DataIngestionConfig
from src.logging.logger import logging
from src.exception.exception import CustomException

def start_data_ingestion():
    try:
        logging.info("Starting Data Ingestion Pipeline...")
        config = DataIngestionConfig()
        ingestion = DataIngestion(config)
        artifacts = ingestion.initiate_data_ingestion()
        logging.info(f"Data Ingestion Completed. Artifacts: {artifacts}")
    except CustomException as ce:
        logging.error(f"CustomException occurred during ingestion: {ce}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        raise CustomException(e, sys)# type: ignore

if __name__ == "__main__":
    start_data_ingestion()
