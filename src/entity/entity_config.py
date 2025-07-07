import os
import sys
from dataclasses import dataclass
from src.constant import constant


@dataclass
class DataIngestionConfig:
    mongo_uri:str =constant.MONGO_URI # type: ignore
    database_name:str=constant.DATABASE_NAME
    collection_name:str=constant.COLLECTION_NAME
    RAW_DATA_FILE_PATH:str=os.path.join(constant.ARTIFACTS_DIR,
                                        constant.FEATURE_STORE_NAME,constant.RAW_DATA_FILE_NAME)
    TRAIN_DATA_FILE_PATH:str=os.path.join(constant.ARTIFACTS_DIR,
                                           constant.INGESTED_NAME,constant.TRAIN_FILE_NAME)
    TEST_DATA_FILE_PATH:str=os.path.join(constant.ARTIFACTS_DIR,constant.INGESTED_NAME,constant.TEST_FILE_NAME)
    TRAIN_TEST_SPLIT_RATIO:float=constant.TRAIN_TEST_SPLIT_RATIO

