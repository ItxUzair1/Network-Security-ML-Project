from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    training_data_path:str
    test_data_path:str