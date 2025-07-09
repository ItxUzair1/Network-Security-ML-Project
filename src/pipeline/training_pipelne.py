import sys
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_train import ModelTrain

from src.entity.entity_config import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainConfig
)

from src.exception.exception import CustomException
from src.logging.logger import logging


def run_training_pipeline():
    try:
        logging.info("Training pipeline started.")

        # 1. Data Ingestion
        logging.info("Step 1: Data Ingestion")
        ingestion_config = DataIngestionConfig()
        ingestion = DataIngestion(config=ingestion_config)
        ingestion_artifacts = ingestion.initiate_data_ingestion()
        logging.info(f"Data Ingestion completed. Artifacts: {ingestion_artifacts}")

        # 2. Data Validation
        logging.info("Step 2: Data Validation")
        validation_config = DataValidationConfig()
        validation = DataValidation(validation_config,ingestion_artifacts)
        validation_artifacts = validation.initiate_data_validation()
        logging.info(f"Data Validation completed. Artifacts: {validation_artifacts}")

        # 3. Data Transformation
        logging.info("Step 3: Data Transformation")
        transformation_config = DataTransformationConfig()
        transformation = DataTransformation(validation_artifacts, transformation_config)
        transformation_artifacts = transformation.initate_transformation()
        logging.info(f"Data Transformation completed. Artifacts: {transformation_artifacts}")

        # 4. Model Training
        logging.info("Step 4: Model Training")
        model_train_config = ModelTrainConfig()
        model_trainer = ModelTrain(data_transforamtion_artifacts=transformation_artifacts, model_train_config=model_train_config)
        model_train_artifacts = model_trainer.initate_model_train()
        logging.info(f"Model Training completed. Artifacts: {model_train_artifacts}")

        logging.info("Training pipeline completed successfully.")

    except CustomException as ce:
        logging.error(f"CustomException occurred during training pipeline: {ce}")
    except Exception as e:
        logging.exception("Unexpected error occurred in training pipeline.")
        raise CustomException(e, sys)  # type: ignore



