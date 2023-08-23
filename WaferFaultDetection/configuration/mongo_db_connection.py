import os
import sys 

import certifi
import pymongo

from WaferFaultDetection.constant import *
from WaferFaultDetection.exception import CustomException

ca = certifi.where()

class MongoDBClient:
    client = None

    def __init__(self, database_name = MONGO_DATABASE_NAME):

        try:
            if MongoDBClient.client is None:
                mongo_db_uri = os.getenv(MONGODB_URI)
                if mongo_db_uri is None:
                    raise Exception('Environment Key : MONGODB_URI is not set.')
                MongoDBClient.client = pymongo.MongoClient(mongo_db_uri, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise CustomException(e, sys)
