from pymongo.mongo_client import MongoClient
import pandas as pd
import json

# uri - uniform resource identifier
uri = "mongodb+srv://Debasish:pa123456pu@cluster0.m2qzamb.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# create_database name and connections
DATABASE_NAME = 'project'
COLLECTION_NAME = 'wafer_fault'

# read the data as a dataFrame
df = pd.read_csv(r'F:\ml project\Wafer_Fault_detection\notebooks\wafer_23012020_041211.csv')
df=df.drop('Unnamed: 0', axis=1)

# convert data ino json
json_record = list(json.loads(df.T.to_json()).values())

# dump the data into the database

client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)

