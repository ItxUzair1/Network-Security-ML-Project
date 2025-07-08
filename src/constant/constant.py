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
SCHEMA_FILE_PATH=os.path.join("schema", "schema.yaml")

DATABASE_NAME = "Network-Security-ML"
COLLECTION_NAME = "Network-Security-ML"
FEATURE_STORE_NAME = "feature_store"
INGESTED_NAME = "ingested"
TRAINED_MODEL_DIR="models"
TRAINED_MODEL_NAME="model.pkl"
EXPECTED_ACCURACY=0.6
MODEL_TRAINED_UNDERFITTING_OVERFITTING=0.05




DATA_VALIDATION_DIR="data_validation"
DATA_VALIDATION_VALID_DIR="valid"
DATA_VALIDATION_INVALID_DIR="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME="drift_report.yaml"

DATA_TRANSFORMATION_DIR="data_transformation"
DATA_TRANSFORMATION_TRAIN_FILE_NAME="train.npy"
DATA_TRANSFORMATION_TEST_FILE_NAME="test.npy"
DATA_TRANSFORMATION_TRANSFORMED_DIR="transformed"
DATA_TRANSFORMATION_PREPROCESSOR_OBJ_DIR="transformed_object"
DATA_TRANSFORMATION_PREPROCESSOR_OBJ_NAME="preprocessor.pkl"
