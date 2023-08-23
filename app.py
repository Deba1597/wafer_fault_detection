import os
import sys

from flask import Flask, render_template, jsonify, request, send_file
from WaferFaultDetection.exception import CustomException
from WaferFaultDetection.logger import logging as lg 

from WaferFaultDetection.pipeline.train_pipeline import TrainingPipeline
from WaferFaultDetection.pipeline.prediction_pipeline import PredictionPipeline

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to my application"


@app.route("/train")
def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()

        return "Training Complete"

    except Exception as e:
        raise CustomException(e, sys)
    
@app.route("/predict", methods=['POST','GET'])
def upload():

    try:
        if request.method == 'POST':
            # it is object of prediction pipeline
            prediction_pipeline = PredictionPipeline(request=request)

            # run the run_pipeline method
            prediction_file_details = prediction_pipeline.run_pipeline()

            lg.info('Prediction completed. downloding prediction file.')
            return send_file(prediction_file_details.prediction_file_path,
                download_name=prediction_file_details.prediction_file_name,
                as_attachment=True)
        else:
            return render_template('upload_file.html')
    
    except Exception as e:
        raise CustomException(e, sys)
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)