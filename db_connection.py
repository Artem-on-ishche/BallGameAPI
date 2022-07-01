from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("CONNECTION_STRING")


def get_database():
    client = MongoClient(CONNECTION_STRING)
    return client.get_database("BallGame")


def get_collection(level_name: str):
    db = get_database()
    return db[level_name]
