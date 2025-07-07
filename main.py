from src.components.data_validation import DataValidation
from src.entity.entity_config import DataValidationConfig
from src.logging.logger import logging
from src.exception.exception import CustomException
from src.entity.entity_config import DataIngestionConfig
from src.components.data_ingestion import DataIngestion

def start_data_ingestion_and_validation():
    try:
        logging.info("🚀 Starting Data Ingestion Pipeline...")
        ingestion_config = DataIngestionConfig()
        ingestion = DataIngestion(ingestion_config)
        ingestion_artifacts = ingestion.initiate_data_ingestion()
        logging.info(f"✅ Data Ingestion Completed. Artifacts: {ingestion_artifacts}")

        logging.info("🚀 Starting Data Validation Pipeline...")
        validation_config = DataValidationConfig()
        validation = DataValidation(validation_config, ingestion_artifacts)
        validation_artifacts = validation.initiate_data_validation()
        logging.info(f"✅ Data Validation Completed. Artifacts: {validation_artifacts}")

    except CustomException as ce:
        logging.error(f"❌ CustomException occurred: {ce}")
    except Exception as e:
        logging.exception("❌ Unexpected error occurred")
        raise CustomException(e, sys)  # type: ignore

if __name__ == "__main__":
    start_data_ingestion_and_validation()
