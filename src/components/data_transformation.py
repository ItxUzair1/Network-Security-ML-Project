import os
import sys
from src.exception.exception import CustomException
from src.logging.logger import logging
import numpy as np
import pandas as pd
from src.entity.artifacts_config import DataValidationArtifacts, DataTransformationArtifacts
from src.entity.entity_config import DataTransformationConfig
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from src.utils.main_utils import save_nparray, save_object
from src.constant.constant import TARGET_COLUMN


class DataTransformation:
    def __init__(self, data_validation_artifacts: DataValidationArtifacts,
                 data_transformation_config: DataTransformationConfig):
        self.data_validation_artifacts = data_validation_artifacts
        self.data_transformation_config = data_transformation_config

    def initate_transformation(self):
        try:
            logging.info("Starting data transformation process.")

            logging.info("Reading validated train and test CSV files.")
            train_data = pd.read_csv(self.data_validation_artifacts.valid_train_path)
            test_data = pd.read_csv(self.data_validation_artifacts.valid_test_path)

            logging.info("Separating input features and target column from training data.")
            train_input = train_data.drop(columns=[TARGET_COLUMN], axis=1)
            train_target = train_data[TARGET_COLUMN].replace(-1, 0)

            logging.info("Separating input features and target column from testing data.")
            test_input = test_data.drop(columns=[TARGET_COLUMN], axis=1)
            test_target = test_data[TARGET_COLUMN].replace(-1, 0)

            logging.info("Creating preprocessing pipeline.")
            preprocessor = self.get_preprocessor_object()

            logging.info("Fitting and transforming training input data.")
            transformed_train_input = preprocessor.fit_transform(train_input)

            logging.info("Transforming testing input data using the fitted preprocessor.")
            transformed_test_input = preprocessor.transform(test_input)

            logging.info("Concatenating transformed input data with target labels.")
            train_arr = np.c_[transformed_train_input, np.array(train_target)]
            test_arr = np.c_[transformed_test_input, np.array(test_target)]

            logging.info("Saving transformed training and testing arrays.")
            save_nparray(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_nparray(self.data_transformation_config.transformed_test_file_path, array=test_arr)

            logging.info("Saving preprocessor object.")
            save_object(self.data_transformation_config.preprocessor_obj_path, obj=preprocessor)

            logging.info("Data transformation completed successfully.")
            return DataTransformationArtifacts(
                preprocessor_obj_path=self.data_transformation_config.preprocessor_obj_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

        except Exception as e:
            logging.error("An error occurred during the data transformation process.")
            raise CustomException(e, sys)#type: ignore

    def get_preprocessor_object(self) -> Pipeline:
        try:
            logging.info("Initializing preprocessing pipeline with KNN imputer.")
            preprocessor = Pipeline(
                steps=[
                    ("imputer", KNNImputer(n_neighbors=3, weights="uniform"))
                ]
            )
            return preprocessor
        except Exception as e:
            logging.error("Failed to create preprocessing pipeline.")
            raise CustomException(e, sys)#type: ignore
