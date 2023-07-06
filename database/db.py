from pymongo import MongoClient
import constants

connection = MongoClient(constants.env["MONGODB_URL"])
db = connection.daggle
print("Connected to DB.")
