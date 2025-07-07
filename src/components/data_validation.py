from src.exception.exception import CustomException
from src.logging.logger import logging
from src.entity.entity_config import DataValidationConfig
import pandas as pd
import sys
from src.constant.constant import SCHEMA_FILE_PATH
from src.entity.artifacts_config import DataIngestionArtifacts, DataValidationArtifacts
from src.utils.utils import read_schema,write_yaml_file
from scipy.stats import ks_2samp
import os

class DataValidation:
    def __init__(self, validation_config: DataValidationConfig, ingestion_artifacts: DataIngestionArtifacts):
        self.validation_config = validation_config
        self.ingestion_artifacts = ingestion_artifacts
        try:
            logging.info("📥 Reading the schema from YAML file...")
            self.schema = read_schema(SCHEMA_FILE_PATH)
            logging.info("✅ Schema successfully loaded.")
        except Exception as e:
            logging.error("❌ Failed to read schema file.")
            raise CustomException(e, sys) # type: ignore
        





    def initiate_data_validation(self) -> DataValidationArtifacts: # type: ignore
        try:
            logging.info("🚀 Initiating data validation process...")

            train_file_path = self.ingestion_artifacts.training_data_path
            test_file_path = self.ingestion_artifacts.test_data_path

            logging.info(f"📄 Reading training data from: {train_file_path}")
            train_df = pd.read_csv(train_file_path)
            logging.info(f"📄 Reading test data from: {test_file_path}")
            test_df = pd.read_csv(test_file_path)

            errors = []

            if not self.validate_number_of_columns(train_df):
                error_msg = "❌ Train columns are not equal to schema."
                logging.error(error_msg)
                errors.append(error_msg)

            if not self.validate_number_of_columns(test_df):
                error_msg = "❌ Test columns are not equal to schema."
                logging.error(error_msg)
                errors.append(error_msg)

            if not self.validate_numerical_columns(train_df):
                error_msg = "❌ Some train dataframe columns are not numeric."
                logging.error(error_msg)
                errors.append(error_msg)

            if not self.validate_numerical_columns(test_df):
                error_msg = "❌ Some test dataframe columns are not numeric."
                logging.error(error_msg)
                errors.append(error_msg)

            validation_status = len(errors) == 0
            if validation_status:
                logging.info("✅ Data validation passed.")
            else:
                logging.warning("⚠️ Data validation failed with errors.")
                for err in errors:
                    logging.warning(f"⚠️ {err}")

            
            report,status=self.detect_data_drift(train_df,test_df)

            os.makedirs(os.path.dirname(self.validation_config.drift_report_file_path), exist_ok=True)

            write_yaml_file(self.validation_config.drift_report_file_path,report)

            valid_train_path=self.validation_config.valid_train_path
            valid_test_path=self.validation_config.valid_test_path

            print(status)

            if status:
                os.makedirs(os.path.dirname(self.validation_config.invalid_train_path), exist_ok=True)
                train_df.to_csv(self.validation_config.invalid_train_path, index=False)
                test_df.to_csv(self.validation_config.invalid_test_path, index=False)

                return DataValidationArtifacts(
                    valid_train_path=None, # type: ignore
                    valid_test_path=None, # type: ignore
                    invalid_train_path=self.validation_config.invalid_train_path,
                    invalid_test_path=self.validation_config.invalid_test_path,
                    drift_report_file_path=self.validation_config.drift_report_file_path,
                    validation_status=False
                )
                
            else:
               
                os.makedirs(os.path.dirname(valid_train_path), exist_ok=True)
                train_df.to_csv(valid_train_path, index=False)
                test_df.to_csv(valid_test_path, index=False)

                return DataValidationArtifacts(
                    valid_train_path=valid_train_path,
                    valid_test_path=valid_test_path,
                    invalid_train_path=None, # type: ignore
                    invalid_test_path=None, # type: ignore
                    drift_report_file_path=self.validation_config.drift_report_file_path,
                    validation_status=True
                )

         

        except Exception as e:
            logging.exception("❌ Exception occurred during data validation.")
            raise CustomException(e, sys)# type: ignore
        



    def validate_number_of_columns(self, df: pd.DataFrame) -> bool:
        try:
            expected_columns = self.schema["columns"]
            if len(df.columns) == len(expected_columns):
                logging.info("✅ Number of columns matched the schema.")
                return True
            else:
                logging.warning(f"Expected {len(expected_columns)} columns but found {len(df.columns)}")
                return False
        except Exception as e:
            logging.exception("❌ Failed during column number validation.")
            raise CustomException(e, sys)# type: ignore

    def validate_numerical_columns(self, df: pd.DataFrame) -> bool:
        try:
            numerical_cols = self.schema["numerical_columns"]
            for col in numerical_cols:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    logging.warning(f"❌ Column '{col}' is not numeric.")
                    return False
            logging.info("✅ All numerical columns are valid.")
            return True
        except Exception as e:
            logging.exception("❌ Failed during numerical column validation.")
            raise CustomException(e, sys) # type: ignore
        


    def detect_data_drift(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> tuple[dict, bool]:
        try:
            logging.info("🔍 Starting KS test for data drift detection...")
            numerical_cols = self.schema["numerical_columns"]
            drift_report = {}
            drift_found = False 

            for col in numerical_cols:
                if col in train_df.columns and col in test_df.columns:
                    statistic, p_value = ks_2samp(train_df[col], test_df[col])
                    drift_detected = p_value < 0.05 # type: ignore
                    if drift_detected:
                        drift_found = True
                    drift_report[col] = {
                        "p_value": p_value,
                        "drift_detected": drift_detected
                    }
                    logging.info(f"📊 Column '{col}': drift_detected={drift_detected}, p_value={p_value:.4f}")
                else:
                    drift_report[col] = {
                        "error": "Column missing in one of the datasets"
                    }
                    logging.warning(f"⚠️ Column '{col}' is missing in train or test set.")

            return drift_report, drift_found

        except Exception as e:
            logging.exception("❌ Failed during KS test.")
            raise CustomException(e, sys)# type: ignore


