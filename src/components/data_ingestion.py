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

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
ca = certifi.where()
@dataclass
class DataIngestionConfig:
    mongo_uri: str = MONGO_URI # type: ignore
    database_name: str = "Network-Security-ML"
    collection_name: str = "Network-Security-ML"
    RAW_DATA_FILE_PATH=os.path.join("artificats","feature_store","phishingData.csv") # type: ignore
    TRAIN_DATA_FILE_PATH=os.path.join("artificats","ingested","train.csv")
    TEST_DATA_FILE_PATH=os.path.join("artificats","ingested","test.csv")
    TRAIN_SPLIT_RATIO: float = 0.8
    TEST_SPLIT_RATIO: float = 0.2

class DataIngestion:
    def __init__(self,config: DataIngestionConfig):
        try:
            logging.info("Connecting to MongoDB")
            self.config = config
            self.client=MongoClient(config.mongo_uri, tlsCAFile=ca)
            self.database=self.config.database_name
            self.collection=self.config.collection_name 
            logging.info("Connected to MongoDB successfully")
        except Exception as e:
            raise CustomException(e, sys) # type: ignore
        
    


    def get_data_from_mongo(self):
        try:
            logging.info("Fetching data from MongoDB")
            data=self.collection.find() # type: ignore
            df = pd.DataFrame(list(data))
            if df.empty:
                raise CustomException("No data found in the MongoDB collection", sys) # type: ignore
            df.reset_index(drop=True, inplace=True)
            logging.info("Data fetched from MongoDB successfully")
            return df
        except Exception as e:
            raise CustomException(e, sys)# type: ignore
