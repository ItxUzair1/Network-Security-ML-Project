import sys
import os
from dotenv import load_dotenv


load_dotenv()
MONGO_URI=os.getenv("MONGO_URI")
if MONGO_URI is None:
    raise ValueError("MONGO_URI environment variable is not set. Please set it in the .env file.")

TARGET_COLUMN = "Result"
ARTIFACTS_DIR="artifacts"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"
RAW_DATA_FILE_NAME="phishingData.csv"
TRAIN_TEST_SPLIT_RATIO = 0.2
TRAINED_MODEL="trained_model.pkl"

DATABASE_NAME = "Network-Security-ML"
COLLECTION_NAME = "Network-Security-ML"
FEATURE_STORE_NAME = "feature_store"
INGESTED_NAME = "ingested"
TRAINED_MODEL_DIR="models"