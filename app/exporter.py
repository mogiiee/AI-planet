import os
from dotenv import load_dotenv

load_dotenv()

#used to get data from dotenv safely and makes code clean

realcluster = os.environ.get("CLUSTER")
db_name = os.environ.get("DB")
collection = os.environ.get("USER_COLLECTION")
hackathon_collection = os.environ.get("HACKATHON_COLLECTION")
submission_collection = os.environ.get("SUBMISSION_COLLECTION")

###COLECTIONS
firebaseApiKey = os.environ.get("apikey")
firebaseAppID = os.environ.get("appId")
databaseURL = os.environ.get("databaseURL")
