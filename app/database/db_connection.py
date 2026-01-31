from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv

load_dotenv()

db_a_client = MongoClient(getenv("FA_MONGO_URI"))

db_a = db_a_client["db_A"]
user_coll = db_a["User"]
todo_coll = db_a["ToDo"]
notification_coll = db_a["Notifications"]
