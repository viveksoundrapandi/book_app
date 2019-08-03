from route.book import book_blueprint
from route.common import common_blueprint
from flask import Flask
from flask.ext.cors import CORS

import config
from model.abc import db

server = Flask(__name__)
server.debug = config.DEBUG

server.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
db.init_app(server)
db.app = server

CORS(
    server,
    resources={r"/*": {"origins": "*"}},
    headers=['Content-Type', 'X-Requested-With', 'Authorization']
)

server.register_blueprint(common_blueprint)

server.register_blueprint(book_blueprint)


if __name__ == '__main__':
    server.run(debug=True, host=config.HOST, port=config.PORT)
