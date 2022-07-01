from flask import Flask
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

CONNECTION_STRING = "mongodb+srv://BallGame:QUj6YfpigrOaCIAZ@ballgamecluster.tmiwe.mongodb.net/?retryWrites=true&w=majority"


class LevelStats(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("level", required=True, type=str, location='args')
        parser.add_argument("player", required=True, type=str, location='args')
        args = parser.parse_args()

        client = MongoClient(CONNECTION_STRING)
        db = client.get_database("BallGame")

        level_name = args["level"]
        collection = db[level_name]

        player_name = args["player"]
        cursor = collection.find().sort("time") if player_name == "*" \
            else collection.find({"player": player_name}).sort("time")

        arr = []
        for doc in cursor:
            arr.append(
                {
                    "player": doc["player"],
                    "time": doc["time"]
                }
            )

        return arr, 400


api.add_resource(LevelStats, '/level_scores')

if __name__ == '__main__':
    app.run()
