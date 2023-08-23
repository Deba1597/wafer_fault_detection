import sys
import os
import numpy as np
import pandas as pd 
from pymongo import MongoClient
from zipfile import Path
from WaferFaultDetection.constant import *
from WaferFaultDetection.exception import CustomException
from WaferFaultDetection.logger import logging
from WaferFaultDetection.utils.main_utils import MainUtils
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    artifact_folder : str = os.path.join(artifact_folder)


class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.utils = MainUtils()

    def export_collection_as_dataframe(self, collection_name, db_name):
        """
        collection name = wafer_fault(data in MongoDB)
        db_name = project (database name in the MongoDB database)
        """
        try:
            mongo_client = MongoClient(MONGODB_URI)

            collection = mongo_client[db_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            if '_id' in df.columns.to_list():
                df = df.drop(columns=['_id'], axis=1)

            df.replace({'na': np.nan}, inplace=True)

            return df
        
        except Exception as e:
            raise CustomException(e, sys) from e

        
    def export_data_into_feature_store_file_path(self) -> pd.DataFrame:
        """
        Method name : export_data_into_feature_store
        description : this method read data from mongodb and save it into artifact.

        Output      : dataste is returned as pd.DataFrame
        on Failure  : Write an exception log and then raise an exception 

        """
        try:
            logging.info(f"Exporting data from mongodb")
            
            raw_file_path = self.data_ingestion_config.artifact_folder
            os.makedirs(raw_file_path, exist_ok=True)

            sensor_data = self.export_collection_as_dataframe(
                                                collection_name=MONGO_COLLECTION_NAME,
                                                db_name=MONGO_DATABASE_NAME
            )

            logging.info(f"Saving exported data into feature stre file path : {raw_file_path}")

            feature_store_file_path = os.path.join(raw_file_path, 'wafer_fault.csv')
            sensor_data.to_csv(feature_store_file_path, index=False)

            return feature_store_file_path
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_ingestion(self) -> Path:
        """
        Method Name   : initiate_data_ingestion
        Description   : This method initiate the data ingestion component of training pipeline

        Output        : train set and test set are returned as the artifact of data ingestion components
        On Failure    : Write an exception log and the raise an exception

        """
        logging.info('Entered initiate_data_ingestion method of DataIngestion Class')

        try:

            feature_store_file_path = self.export_data_into_feature_store_file_path()

            logging.info('Got the data from MongoDB')

            logging.info('Exited initiate_data_ingestion method of Data_ingestion Class')

            return feature_store_file_path
        
        except Exception as e:
            raise CustomException(e, sys)

                