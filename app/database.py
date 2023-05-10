from . import exporter
import pymongo


cluster = pymongo.MongoClient(exporter.realcluster)

db = cluster[exporter.db_name]

user_collection = db[exporter.collection]
