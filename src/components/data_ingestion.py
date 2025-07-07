import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi
import pandas as pd
import numpy as np
from src.exception.exception import CustomException
from src.logging.logger import logging
from dataclasses import dataclass
from src.entity.entity_config import DataIngestionConfig # type: ignore
from sklearn.model_selection import train_test_split
from src.entity.artifacts_config import DataIngestionArtifacts



class DataIngestion:
    def __init__(self,config: DataIngestionConfig):
        try:
            logging.info("Loading Data Ingestion Configuration")
            self.config = config

        except Exception as e:
            raise CustomException(e, sys) # type: ignore
        
    


    def get_data_from_mongo(self):
        try:
            logging.info("Fetching data from MongoDB")
            databse_name=self.config.database_name
            collection_name=self.config.collection_name
            client=MongoClient(self.config.mongo_uri)
            data= client[databse_name][collection_name].find()
            df = pd.DataFrame(list(data))
            if df.empty:
                raise CustomException("No data found in the MongoDB collection", sys) # type: ignore
            df.reset_index(drop=True, inplace=True)
            df.replace({"na":np.nan}, inplace=True)
            logging.info("Data fetched from MongoDB successfully")
            return df
        except Exception as e:
            raise CustomException(e, sys)# type: ignore


    def initiate_data_ingestion(self):
        try:
            dataframe=self.get_data_from_mongo()
            logging.info("Initiating data ingestion process")
            if dataframe.empty:
                raise CustomException("Dataframe is empty. No data to save.", sys) # type: ignore
            self.save_data_into_feature_store(dataframe)
            self.split_data(dataframe)
            data_artifacts=DataIngestionArtifacts(training_data_path=self.config.TRAIN_DATA_FILE_PATH,
                                                   test_data_path=self.config.TEST_DATA_FILE_PATH)
            return data_artifacts

            
        except Exception as e:
            raise CustomException(e, sys) # type: ignore
        

    def save_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            logging.info("Saving data into feature store")
            dir_name=os.path.dirname(self.config.RAW_DATA_FILE_PATH)
            os.makedirs(dir_name, exist_ok=True)
            dataframe.to_csv(self.config.RAW_DATA_FILE_PATH, index=False)
            logging.info(f"Data saved into feature store at {self.config.RAW_DATA_FILE_PATH}")
        except Exception as e:
            raise CustomException(e, sys) # type: ignore
        

    def split_data(self, dataframe: pd.DataFrame):
        try:
            logging.info("Splitting data into train and test sets")
            if dataframe.empty:
                raise CustomException("Dataframe is empty. Cannot split data.", sys) # type: ignore
            train_dir=os.path.dirname(self.config.TRAIN_DATA_FILE_PATH)
            test_dir=os.path.dirname(self.config.TEST_DATA_FILE_PATH)
            os.makedirs(train_dir, exist_ok=True)
            os.makedirs(test_dir, exist_ok=True)

            train_set, test_set = train_test_split(dataframe, test_size=self.config.TRAIN_TEST_SPLIT_RATIO, random_state=42)

            train_set.to_csv(self.config.TRAIN_DATA_FILE_PATH, index=False)
            test_set.to_csv(self.config.TEST_DATA_FILE_PATH, index=False)
            logging.info(f"Train data saved at {self.config.TRAIN_DATA_FILE_PATH}")
            logging.info(f"Test data saved at {self.config.TEST_DATA_FILE_PATH}")

        except Exception as e:
            raise CustomException(e, sys) # type: ignore
