import sys 
import os
import pandas as pd

from WaferFaultDetection.component.data_ingestion import DataIngestion
from WaferFaultDetection.component.data_transformation import DataTransformation
from WaferFaultDetection.component.model_trainer import ModelTrainer
from WaferFaultDetection.exception import CustomException
from WaferFaultDetection.logger import logging


class TrainingPipeline:

    def start_data_ingestion(self):
        
        logging.info('Data ingestion start')

        try:
            data_ingestion = DataIngestion()
            feature_store_file_path = data_ingestion.initiate_data_ingestion()

            return feature_store_file_path
        
        except Exception as e:
            raise CustomException(e, sys)

    
    def start_data_transformation(self, feature_store_file_path):
        
        logging.info('Data Transform start')

        try:
            data_transformation = DataTransformation(feature_store_file_path=feature_store_file_path)
            train_arr, test_arr, preprocessor_path = data_transformation.initiate_data_transformation()

            return train_arr, test_arr, preprocessor_path

        except Exception as e:
            raise CustomException(e, sys)

    
    def start_model_training(self, train_arr,test_arr):

        logging.info('Model training start.')

        try:
            model_trainer = ModelTrainer()
            model_score = model_trainer.initiate_model_trainer(
                train_array=train_arr,
                test_array=test_arr
            )
            return model_score
        
        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self):
        try: 
            feature_store_file_path = self.start_data_ingestion()
            train_arr, test_arr, preprocessor_path = self.start_data_transformation(feature_store_file_path=feature_store_file_path)

            r2_square = self.start_model_training(train_arr=train_arr,test_arr=test_arr)

            print(f'Training completed. Trained model score : {r2_square}')

        except Exception as e:
            raise CustomException(e,sys)