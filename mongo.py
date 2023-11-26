
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

uri = os.environ['MONGOPATH']

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

DataDB = client['Data']
collection = DataDB['DataDB']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
