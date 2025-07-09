from flask import Flask, jsonify,request,render_template
from src.pipeline.training_pipelne import run_training_pipeline
from src.exception.exception import CustomException
from src.logging.logger import logging
import sys
import pandas as pd
import numpy as np
from src.utils.main_utils import load_object
from src.utils.model_utils import NetworkModel
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/train", methods=["GET"])
def train_model():
    try:
        logging.info("Received request to start training pipeline.")
        run_training_pipeline()
        return jsonify({"message": "Training pipeline executed successfully."}), 200
    except CustomException as ce:
        logging.error(f"CustomException occurred: {ce}")
        return jsonify({"error": str(ce)}), 500
    except Exception as e:
        logging.exception("Unexpected error occurred during training.")
        return jsonify({"error": "An unexpected error occurred."}), 500
    
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.form.to_dict()

        # Ensure all values are integers
        input_data = {k: int(v) for k, v in data.items()}

        df = pd.DataFrame([input_data])

        model = load_object("models/model.pkl")
        preprocessor = load_object("models/preprocessor.pkl")

        network_model = NetworkModel(preprocessor, model)
        prediction = network_model.predict(df)

        result = "Phishing" if prediction[0] == 0 else "Legitimate"

        return jsonify({"prediction": int(prediction[0]), "result": result})

    except Exception as e:
        raise CustomException(e, sys)  # type: ignore

if __name__ == '__main__':
    try:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logging.error(f"Error starting the Flask app: {e}")
        raise CustomException(e,sys) # type: ignore