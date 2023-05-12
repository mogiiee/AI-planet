import os
from dotenv import load_dotenv

load_dotenv()


realcluster = os.environ.get("CLUSTER")
db_name = os.environ.get("DB")
collection = os.environ.get("USER_COLLECTION")
hackathon_collection = os.environ.get("HACKATHON_COLLECTION")

###COLECTIONS
firebaseApiKey = os.environ.get("apikey")
firebaseAppID = os.environ.get("appId")

