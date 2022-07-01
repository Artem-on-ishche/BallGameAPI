from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://BallGame:QUj6YfpigrOaCIAZ@ballgamecluster.tmiwe.mongodb.net/?retryWrites=true&w=majority"


def get_database():
    client = MongoClient(CONNECTION_STRING)
    return client.get_database("BallGame")


def get_collection(level_name: str):
    db = get_database()
    return db[level_name]