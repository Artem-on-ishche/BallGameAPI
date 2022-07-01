from flask import Flask
from flask_restful import Resource, Api, reqparse

from db_connection import get_collection

app = Flask(__name__)
api = Api(app)


class LevelStats(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("level", required=True, type=str, location='args')
        parser.add_argument("player", required=True, type=str, location='args')
        args = parser.parse_args()

        level_name = args["level"]
        collection = get_collection(level_name)

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

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("level", required=True, type=str, location='args')
        parser.add_argument("player", required=True, type=str, location='args')
        parser.add_argument("time", required=True, type=float, location='args')
        args = parser.parse_args()

        level_name = args["level"]
        collection = get_collection(level_name)

        collection.insert_one(
            {
                "player": args["player"],
                "time": args["time"]
            }
        )

        return 400


api.add_resource(LevelStats, '/level_scores')

if __name__ == '__main__':
    app.run()
