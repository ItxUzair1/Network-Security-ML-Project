import yaml
from src.exception.exception import CustomException
from src.logging.logger import logging
import os

def read_schema(file_path) -> dict:
    try:
        with open(file_path,"rb") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise CustomException(e,sys)# type: ignore
    


def write_yaml_file(file_path: str, data: dict) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
        print(f"✅ YAML file written to: {file_path}")
    except Exception as e:
        print(f"❌ Failed to write YAML file: {e}")
        raise
