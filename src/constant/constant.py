import sys
import os
from dotenv import load_dotenv


load_dotenv()
MONGO_URI=os.getenv("MONGO_URI")
if MONGO_URI is None:
    raise ValueError("MONGO_URI environment variable is not set. Please set it in the .env file.")

TARGET_COLUMN = "Result"
ARTIFACTS_DIR="artifacts"
DATA_INGESTION_DIR="data_ingestion"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"
RAW_DATA_FILE_NAME="phishingData.csv"
TRAIN_TEST_SPLIT_RATIO = 0.2
TRAINED_MODEL="trained_model.pkl"
SCHEMA_FILE_PATH=os.path.join("schema", "schema.yaml")

DATABASE_NAME = "Network-Security-ML"
COLLECTION_NAME = "Network-Security-ML"
FEATURE_STORE_NAME = "feature_store"
INGESTED_NAME = "ingested"
TRAINED_MODEL_DIR="models"



DATA_VALIDATION_DIR="data_validation"
DATA_VALIDATION_VALID_DIR="valid"
DATA_VALIDATION_INVALID_DIR="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME="drift_report.yaml"