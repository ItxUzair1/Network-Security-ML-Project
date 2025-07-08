import sys
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation

from src.entity.entity_config import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig
)
from src.exception.exception import CustomException
from src.logging.logger import logging


def start_pipeline():
    try:
        # Step 1: Data Ingestion
        logging.info("🚀 Starting Data Ingestion Pipeline...")
        ingestion_config = DataIngestionConfig()
        ingestion = DataIngestion(ingestion_config)
        ingestion_artifacts = ingestion.initiate_data_ingestion()
        logging.info(f"✅ Data Ingestion Completed. Artifacts: {ingestion_artifacts}")

        # Step 2: Data Validation
        logging.info("🚀 Starting Data Validation Pipeline...")
        validation_config = DataValidationConfig()
        validation = DataValidation(validation_config, ingestion_artifacts)
        validation_artifacts = validation.initiate_data_validation()
        logging.info(f"✅ Data Validation Completed. Artifacts: {validation_artifacts}")

        # Step 3: Data Transformation
        logging.info("🚀 Starting Data Transformation Pipeline...")
        transformation_config = DataTransformationConfig()
        transformation = DataTransformation(validation_artifacts, transformation_config)
        transformation_artifacts = transformation.initate_transformation()
        logging.info(f"✅ Data Transformation Completed. Artifacts: {transformation_artifacts}")

    except CustomException as ce:
        logging.error(f"❌ CustomException occurred: {ce}")
    except Exception as e:
        logging.exception("❌ Unexpected error occurred")
        raise CustomException(e, sys)  # type: ignore


if __name__ == "__main__":
    start_pipeline()
