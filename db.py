from pymongo import MongoClient

client = MongoClient()
db = client["finviz"]
