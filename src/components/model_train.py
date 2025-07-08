import os
import sys
from src.exception.exception import CustomException
from src.logging.logger import logging
from sklearn.model_selection import train_test_split
from src.entity.entity_config import ModelTrainConfig
from src.entity.artifacts_config import DataTransformationArtifacts,ModelTrainArtifacts
from src.utils.main_utils import save_object,load_object,load_numpy_array,evaluate_model
from src.utils.metric_utils import get_classification_report
from src.utils.model_utils import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,AdaBoostClassifier
from xgboost import XGBClassifier


class ModelTrain():
    def __init__(self, data_transforamtion_artifacts: DataTransformationArtifacts,
                 model_train_config: ModelTrainConfig):
        self.data_transformation_artifacts = data_transforamtion_artifacts
        self.model_train_config = model_train_config

    def initate_model_train(self):
        try:
            logging.info("Loading transformed training and test data arrays.")
            train_data = load_numpy_array(self.data_transformation_artifacts.transformed_train_file_path)
            test_data = load_numpy_array(self.data_transformation_artifacts.transformed_test_file_path)

            X_train, y_train = train_data[:, :-1], train_data[:, -1]
            X_test, y_test = test_data[:, :-1], test_data[:, -1]

            logging.info("Initiating model training and tuning.")
            model_train_artifacts = self.train_model(X_train, y_train, X_test, y_test)
            logging.info("Model training completed successfully.")
            return model_train_artifacts

        except Exception as e:
            logging.error("Exception occurred during model training initiation.")
            raise CustomException(e, sys)# type: ignore

    def train_model(self, X_train, y_train, X_test, y_test):
        logging.info("Defining models and hyperparameters.")
        models = {
            "LogisticRegression": LogisticRegression(),
            "KNN": KNeighborsClassifier(),
            "Support Vector Machine": SVC(),
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier(),
            "AdaBoost": AdaBoostClassifier(),
            "GradientBoosting": GradientBoostingClassifier(),
            "XgBoost": XGBClassifier()
        }

        params = {
            "LogisticRegression": {
                "penalty": ["l1", "l2", "elasticnet", None],
                "C": [0.01, 0.1, 1, 10],
                "solver": ["liblinear", "saga"],
                "max_iter": [100, 200, 500]
            },
            "KNN": {
                "n_neighbors": [3, 5, 7, 9],
                "weights": ["uniform", "distance"],
                "metric": ["euclidean", "manhattan", "minkowski"]
            },
            "Support Vector Machine": {
                "C": [0.1, 1, 10, 100],
                "kernel": ["linear", "rbf", "poly", "sigmoid"],
                "gamma": ["scale", "auto"]
            },
            "Decision Tree": {
                "criterion": ["gini", "entropy", "log_loss"],
                "max_depth": [None, 5, 10, 20],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4]
            },
            "Random Forest": {
                "n_estimators": [50, 100, 200],
                "criterion": ["gini", "entropy", "log_loss"],
                "max_depth": [None, 10, 20],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
                "bootstrap": [True, False]
            },
            "AdaBoost": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.1, 1]
            },
            "GradientBoosting": {
                "n_estimators": [100, 200],
                "learning_rate": [0.01, 0.1, 0.2],
                "max_depth": [3, 5, 7],
                "subsample": [0.8, 1.0]
            },
            "XgBoost": {
                "n_estimators": [100, 200],
                "learning_rate": [0.01, 0.1, 0.2],
                "max_depth": [3, 5, 7],
                "subsample": [0.8, 1.0],
                "colsample_bytree": [0.6, 0.8, 1.0],
                "gamma": [0, 0.1, 0.2]
            }
        }

        logging.info("Evaluating models using RandomizedSearchCV.")
        report, best_models = evaluate_model(X_train, y_train, X_test, y_test, models, params)
        print(report)

        best_model_name = max(report, key=lambda name: report[name]["accuracy"])
        model = best_models[best_model_name]

        logging.info(f"Best model selected: {best_model_name} with accuracy {report[best_model_name]['accuracy']:.4f}")

        logging.info("Generating classification report for training data.")
        train_pred = model.predict(X_train)
        classification_train_report = get_classification_report(y_train, train_pred)

        logging.info("Generating classification report for test data.")
        test_pred = model.predict(X_test)
        classification_test_report = get_classification_report(y_test, test_pred)

        logging.info("Loading preprocessor object.")
        preprocessor = load_object(self.data_transformation_artifacts.preprocessor_obj_path)

        logging.info("Creating and saving NetworkModel object.")
        network_obj = NetworkModel(preprocessor, model)
        save_object(self.model_train_config.train_model_path, network_obj)

        logging.info("Model and preprocessing pipeline saved successfully.")
        return ModelTrainArtifacts(
            self.data_transformation_artifacts.preprocessor_obj_path,
            self.model_train_config.train_model_path,
            classification_train_report,
            classification_test_report
        )



