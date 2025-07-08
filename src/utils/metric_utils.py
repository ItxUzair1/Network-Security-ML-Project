from src.exception.exception import CustomException
from src.entity.artifacts_config import ClassificationReportArtifacts
from sklearn.metrics import f1_score,precision_score,recall_score


def get_classification_report(y_true,y_pred)->ClassificationReportArtifacts: # type: ignore
    try:
        model_f1=f1_score(y_true,y_pred)
        model_precision=precision_score(y_true,y_pred)
        model_recall=recall_score(y_true,y_pred)

        report= ClassificationReportArtifacts(model_f1,model_precision,model_recall) # type: ignore
        return report
    except Exception as e:
        raise CustomException(e,sys)# type: ignore