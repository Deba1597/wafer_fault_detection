import sys
import os
from typing import Dict, Tuple
import pandas as pd 
import pickle
import yaml
import boto3

from WaferFaultDetection.constant import *
from WaferFaultDetection.exception import CustomException
from WaferFaultDetection.logger import logging

class MainUtils:
    def __init__(self):
        pass

    def read_yaml_file(self, filename:str)->Dict:
        try:
            with open(filename, 'rb') as yaml_file:
                return yaml.safe_load(yaml_file)
        
        except Exception as e:
            raise CustomException(e, sys) from e

    def read_schema_config_file(self) -> Dict:
        try:
            schema_config = self.read_yaml_file(os.path.join('config','schema.yaml'))

            return schema_config
        
        except Exception as e:
            raise CustomException(e, sys) from e
    
    @staticmethod
    def save_object(file_path : str, obj:object) -> None:
        logging.info('Entered the save_object method of MainUtils class')

        try:
            with open(file_path, 'wb') as file_obj:
                pickle.dump(obj, file_obj)

            logging.info('Exited the save_object method of MainUtils class')
        
        except Exception as e:
            raise CustomException(e, sys) from e

    
    @staticmethod
    def load_object(file_path:str) -> object:
        logging.info("Entered the load_object method of MainUtils class")

        try:
            with open(file_path, 'rb') as file_obj:
                obj = pickle.load(file_obj)
            
            logging.info('Exited te load_object method of MainUtils class')
            
            return obj
        
        except Exception as e:
            raise CustomException(e, sys) from e

    # @staticmethod
    # def load_object(file_path):
    #     try:
    #         with open(file_path, 'rb') as file_obj:
    #             return pickle.load(file_obj)
    #     except Exception as e:
    #         raise CustomException(e, sys) from e