import yaml
from src.exception.exception import CustomException
from src.logging.logger import logging
import os
import numpy as np
import pickle
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score

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
        print(f"YAML file written to: {file_path}")
    except Exception as e:
        print(f"Failed to write YAML file: {e}")
        raise


def save_nparray(file_path:str,array:np.ndarray):
    try:
        logging.info("Saving the np arrays")
        dir=os.path.dirname(file_path)
        os.makedirs(dir,exist_ok=True)

        with open(file_path,"wb") as file:
            np.save(file,array)
        
        logging.info("Sucessfully saved thenp array")
    except Exception as e:
        raise CustomException(e,sys)# type: ignore


def save_object(file_path:str,obj:object):
    try:
        logging.info("Saving the pkl file")
        dir=os.path.dirname(file_path)
        os.makedirs(dir,exist_ok=True)

        with open(file_path,"wb") as file:
            pickle.dump(obj,file)
        
        logging.info("Successfully saved the pkl file")
    except Exception as e:
        raise CustomException(e,sys)# type: ignore
    

def load_object(file_path: str):
    """
    Loads a Python object from a pickle (.pkl) file.

    Args:
        file_path (str): Path to the pickle file.

    Returns:
        object: The loaded Python object.

    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: If loading fails for another reason.
    """
    if not os.path.exists(file_path):
        logging.error(f"Pickle file not found at path: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, "rb") as file_obj:
            obj = pickle.load(file_obj)
            logging.info(f"Successfully loaded pickle object from {file_path}")
            return obj
    except Exception as e:
        logging.exception(f"Error loading pickle file from {file_path}")
        raise Exception(f"Error loading pickle file: {e}")

def load_numpy_array(file_path: str):
    """
    Loads a NumPy array from a .npy file.

    Args:
        file_path (str): Path to the NumPy file.

    Returns:
        np.ndarray: The loaded NumPy array.

    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: If loading fails for another reason.
    """
    if not os.path.exists(file_path):
        logging.error(f"NumPy file not found at path: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, "rb") as file:
            array = np.load(file)
            logging.info(f"Successfully loaded NumPy array from {file_path}")
            return array
    except Exception as e:
        logging.exception(f"Error loading NumPy array from {file_path}")
        raise Exception(f"Error loading NumPy array: {e}")

def evaluate_model(X_train, y_train, X_test, y_test, models: dict, params: dict, n_iter=10, cv=3):
    try:
        report = {}
        best_models = {}

        for model_name, model in models.items():
            param = params.get(model_name, {})

            rs = RandomizedSearchCV(model, param_distributions=param, n_iter=n_iter, cv=cv, 
                                    scoring='accuracy', n_jobs=-1, random_state=42, verbose=0)
            rs.fit(X_train, y_train)

            best_model = rs.best_estimator_
            y_pred = best_model.predict(X_test) # type: ignore
            score = accuracy_score(y_test, y_pred)

            report[model_name] = {
                "accuracy": score,
                "best_params": rs.best_params_
            }

            best_models[model_name] = best_model

    except Exception as e:
        raise CustomException(e, sys)  # type: ignore

    return report, best_models