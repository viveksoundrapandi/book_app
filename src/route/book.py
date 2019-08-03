from resource.book import BookAPI, BookListAPI, BookExternalAPI
from flask import Blueprint
from flask.ext.restful import Api


book_blueprint = Blueprint('book', __name__)
book_blueprint_api = Api(book_blueprint)


book_blueprint_api.add_resource(BookListAPI, '/api/v1/books/')
book_blueprint_api.add_resource(BookAPI, '/api/v1/books/<int:id>')
book_blueprint_api.add_resource(BookExternalAPI, '/api/external-books/')
