from src.exception.exception import CustomException
import sys


class NetworkModel():
    def __init__(self,preprocessor,model):
        self.preprocessor=preprocessor
        self.model=model

    
    def predict(self,X):
        try:
            transformed_data=self.preprocessor.transform(X)
            predictions=self.model.predict(transformed_data)
            return predictions
        except Exception as e:
            raise CustomException(e,sys)# type: ignore