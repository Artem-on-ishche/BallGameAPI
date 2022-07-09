from flask import Response
from flask_restful import Resource, reqparse

from db_connection import get_collection


class Nicknames(Resource):

    def get(self):
        nicknames = []
        cursor = get_collection("Nicknames").find()

        for item in cursor:
            nicknames.append(item["nickname"])

        return nicknames, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("nickname", required=True, type=str, location='args')
        args = parser.parse_args()
        nickname = args["nickname"]

        collection = get_collection("Nicknames")

        if collection.find_one({"nickname": nickname}) is not None:
            return Response(status=409)

        collection.insert_one({
            "nickname": args["nickname"],
        })

        return Response(status=200)
