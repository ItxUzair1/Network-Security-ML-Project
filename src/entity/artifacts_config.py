from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    training_data_path:str
    test_data_path:str


@dataclass
class DataValidationArtifacts:
    valid_train_path:str
    valid_test_path:str
    invalid_train_path:str
    invalid_test_path:str
    drift_report_file_path:str
    validation_status:bool
    


@dataclass
class DataTransformationArtifacts:
    preprocessor_obj_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str