from flask import Flask
from flask_restful import Api

from level_stats import LevelStats
from nicknames import Nicknames

app = Flask(__name__)
api = Api(app)

api.add_resource(LevelStats, '/level_scores')
api.add_resource(Nicknames, '/nicknames')

if __name__ == '__main__':
    app.run()
