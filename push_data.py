import os
import json
import json
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi
import pandas as pd
import numpy as np
from src.exception.exception import CustomException
from src.logging.logger import logging
import requests

load_dotenv()
MONGO_URI=os.getenv("MONGO_URI")
ca = certifi.where()

class NetworkSecurityExtract:
    def __init__(self):
        try:
            logging.info("Connecting to MoongoDB")
            self.client=MongoClient(MONGO_URI, tlsCAFile=ca)
            self.database=self.client["Network-Security-ML"]
            self.collection=self.database["Network-Security-ML"]
            logging.info("Connected to MongoDB successfully")
        except Exception as e:
            raise CustomException(e, sys) # type: ignore
        

    
    def csv_to_json(self,csv_path):
        try:
            logging.info("Converting CSV to JSON")
            df = pd.read_csv(csv_path)
            df.reset_index(drop=True, inplace=True)
            json_data=json.loads(df.to_json(orient='records'))
            return json_data
        except Exception as e:
            raise CustomException(e, sys) # type: ignore
        

    def push_data(self, json_data):
        try:
            logging.info("Pushing data to MongoDB")
            if isinstance(json_data, list):
                self.collection.insert_many(json_data)
            else:
                self.collection.insert_one(json_data)
            logging.info("Data pushed to MongoDB successfully")
        
        except Exception as e:
            raise CustomException(e, sys) # type: ignore
            logging.error("Error pushing data to MongoDB")


if __name__ == "__main__":
    try:
        logging.info("Starting pushing data to MongoDB")
        obj=NetworkSecurityExtract()
        FILE_PATH=os.path.join("data","phisingData.csv")
        json_data=obj.csv_to_json(FILE_PATH)
        obj.push_data(json_data)
        logging.info("Data pushed successfully")
    except Exception as e:
        logging.error("An error occurred in the main block")
        raise CustomException(e, sys) # type: ignore