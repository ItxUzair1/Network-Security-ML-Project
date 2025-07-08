import os
import sys
from dataclasses import dataclass
from src.constant import constant


@dataclass
class DataIngestionConfig:
    mongo_uri:str =constant.MONGO_URI # type: ignore
    database_name:str=constant.DATABASE_NAME
    collection_name:str=constant.COLLECTION_NAME
    RAW_DATA_FILE_PATH:str=os.path.join(constant.ARTIFACTS_DIR,constant.DATA_INGESTION_DIR,
                                        constant.FEATURE_STORE_NAME,constant.RAW_DATA_FILE_NAME)
    TRAIN_DATA_FILE_PATH:str=os.path.join(constant.ARTIFACTS_DIR,constant.DATA_INGESTION_DIR,
                                           constant.INGESTED_NAME,constant.TRAIN_FILE_NAME)
    TEST_DATA_FILE_PATH:str=os.path.join(constant.ARTIFACTS_DIR,constant.DATA_INGESTION_DIR,constant.INGESTED_NAME,constant.TEST_FILE_NAME)
    TRAIN_TEST_SPLIT_RATIO:float=constant.TRAIN_TEST_SPLIT_RATIO



class DataValidationConfig():
    def __init__(self):
        self.data_validation_dir=os.path.join(constant.ARTIFACTS_DIR,constant.DATA_VALIDATION_DIR)
        self.valid_dir=os.path.join(self.data_validation_dir,constant.DATA_VALIDATION_VALID_DIR)
        self.invalid_dir=os.path.join(self.data_validation_dir,constant.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_path=os.path.join(self.valid_dir,constant.TRAIN_FILE_NAME)
        self.valid_test_path=os.path.join(self.valid_dir,constant.TEST_FILE_NAME)
        self.invalid_train_path=os.path.join(self.invalid_dir,constant.TRAIN_FILE_NAME)
        self.invalid_test_path=os.path.join(self.invalid_dir,constant.TEST_FILE_NAME)
        self.drift_report_dir=os.path.join(self.data_validation_dir,constant.DATA_VALIDATION_DRIFT_REPORT_DIR)
        self.drift_report_file_path=os.path.join(self.drift_report_dir,constant.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)


class DataTransformationConfig():
    def __init__(self):
        self.data_transformation_dir=os.path.join(constant.ARTIFACTS_DIR,constant.DATA_TRANSFORMATION_DIR)
        self.transforemd_train_file_path=os.path.join(self.data_transformation_dir,constant.DATA_TRANSFORMATION_TRANSFORMED_DIR,constant.DATA_TRANSFORMATION_TRAIN_FILE_NAME)
        self.transforemd_test_file_path=os.path.join(self.data_transformation_dir,constant.DATA_TRANSFORMATION_TRANSFORMED_DIR,constant.DATA_TRANSFORMATION_TEST_FILE_NAME)
        self.preprocessor_obj_path=os.path.join(self.data_transformation_dir,constant.DATA_TRANSFORMATION_PREPROCESSOR_OBJ_DIR,constant.DATA_TRANSFORMATION_PREPROCESSOR_OBJ_NAME)
        


