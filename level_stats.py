from datetime import datetime
from flask_restful import Resource, reqparse

from db_connection import get_collection


def get_utc_time():
    return datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC")


# get
# https://practice-ball-game.herokuapp.com/level_scores?level=Level00&player_nickname=*&entries_count=0
#
# post
# https://practice-ball-game.herokuapp.com/level_scores?level=Level00&player_nickname=deez_nutser&level_time=19.01

class LevelStats(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("level", required=True, type=str, location='args')
        parser.add_argument("player_nickname", required=True, type=str, location='args')
        parser.add_argument("entries_count", required=True, type=int, location='args')
        args = parser.parse_args()

        level_name = args["level"]
        collection = get_collection(level_name)

        player_name = args["player_nickname"]
        cursor = collection.find().sort("level_time") if player_name == "*" \
            else collection.find({"player_nickname": player_name}).sort("level_time")

        entries_count = args["entries_count"]

        arr = []
        count = 0
        for doc in cursor:
            if 0 < entries_count == count:
                break

            arr.append(
                {
                    "player_nickname": doc["player_nickname"],
                    "level_time": doc["level_time"],
                    "completion_datetime": doc["completion_datetime"]
                }
            )

            count += 1

        return arr, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("level", required=True, type=str, location='args')
        parser.add_argument("player_nickname", required=True, type=str, location='args')
        parser.add_argument("level_time", required=True, type=float, location='args')
        args = parser.parse_args()

        level_name = args["level"]
        collection = get_collection(level_name)

        collection.insert_one({
            "player_nickname": args["player_nickname"],
            "level_time": args["level_time"],
            "completion_datetime": get_utc_time()
        })

        return {}
