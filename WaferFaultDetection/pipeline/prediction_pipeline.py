import shutil
import os
import pickle
import sys
import pandas as pd

from WaferFaultDetection.logger import logging
from WaferFaultDetection.exception import CustomException
from WaferFaultDetection.utils.main_utils import MainUtils
from WaferFaultDetection.constant import *

from flask import request
from dataclasses import dataclass

@dataclass
class PredictionPipelineConfig:
    prediction_output_dirname = 'predictions'
    prediction_file_name = 'predicted_file.csv'
    model_file_path : str = os.path.join(artifact_folder, 'model.pkl')
    preprocessor_path : str = os.path.join(artifact_folder, 'preprocessor.pkl')
    prediction_file_path : str = os.path.join(prediction_output_dirname, prediction_file_name)


class PredictionPipeline:
    def __init__(self, request=request):

        self.request = request
        self.utils = MainUtils()
        self.prediction_pipeline_config = PredictionPipelineConfig() 

    def save_input_files(self)->str:
        """
        Method name   : save_input_files
        Description   : This method saves the input file to the prediction artifact directory

        Output        : file path
        On Failure    : Write an exception log and then raise an exception

        """

        try: 
            #creating the file
            pred_file_input_dir = "prediction_artifact"
            os.makedirs(pred_file_input_dir, exist_ok=True)

            input_csv_file = self.request.files['file']
            pred_file_path = os.path.join(pred_file_input_dir, input_csv_file.filename)

            input_csv_file.save(pred_file_path)

            return pred_file_path
        except Exception as e:
            raise CustomException(e, sys)

    
    def predict(self, features):

        try: 
            model = self.utils.load_object(self.prediction_pipeline_config.model_file_path)
            preprocessor = self.utils.load_object(self.prediction_pipeline_config.preprocessor_path)

            transformed_x = preprocessor.transform(features)

            preds = model.predict(transformed_x)

            return preds
        
        except Exception as e:
            raise CustomException(e, sys)

    def get_predicted_dataframe(self, input_dataframe_path):

        """
        Method Name   : get_predicted_dataframe
        Description   : this method return the dataframe with a new column containing predictions

        Output        : Predicted dataframe
        On Failure    : Write an exception log and then raise an exception
        """
        try:

            prediction_column_name : str = TARGET_COLUMN
            input_dataframe : pd.DataFrame = pd.read_csv(input_dataframe_path)

            input_dataframe = input_dataframe.drop(columns='Unnamed: 0') if 'Unnamed: 0' in input_dataframe.columns else input_dataframe

            predictions = self.predict(input_dataframe)
            input_dataframe[prediction_column_name] = [pred for pred in predictions]

            target_column_mapping = {0:'Bad', 1:'Good'}

            input_dataframe[prediction_column_name] = input_dataframe[prediction_column_name].map(target_column_mapping)

            os.makedirs(self.prediction_pipeline_config.prediction_output_dirname, exist_ok=True)
            input_dataframe.to_csv(self.prediction_pipeline_config.prediction_file_path, index=False)

            logging.info(f"Prediction Complete")

        except Exception as e:
            raise CustomException(e, sys) from e

    def run_pipeline(self):

        try:
            input_csv_path = self.save_input_files() 
            self.get_predicted_dataframe(input_csv_path)

            return self.prediction_pipeline_config
        
        except Exception as e:
            raise CustomException(e, sys)
            