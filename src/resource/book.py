from flask import jsonify, request
from flask.ext.restful import Resource
from werkzeug.exceptions import BadRequest
import traceback
from sqlalchemy import exc

from wiring import *
from model.abc import db
from model import Book, Author, BookAuthorLink


class BookAPI(Resource):
    def get(self, id):
        book = Book.find_by_id(id)
        return {
            "status_code": 200,
            "status": "success",
            "data": {} if book is None else book.json()
        }

    def patch(self, id):
        book = Book.find_by_id(id)
        if book is None:
            self._raise_bad_request("Book Not Found")
        try:
            json_data = request.get_json(force=True)
            book.update(json_data)
            db.session.commit()
            return {
                "status_code": 200,
                "status": "success",
                "data": book.json()
            }
        except (ValueError) as e:
            db.session().rollback()
            res = BadRequest(e.message)
            res.data = {'message': e.message}
            raise res

    def delete(self, id):
        book = Book.find_by_id(id)
        if book is None:
            self._raise_bad_request("Book Not Found")
        book_name = book.name
        book.delete()
        return {
            "status_code": 200,
            "status": "success",
            "data": [],
            "message": "The book {:s} was deleted successfully".format(book_name)
        }

    def _raise_bad_request(self, message):
        res = BadRequest("Book Not Found")
        res.data = {'message': "Book Not Found!"}
        raise res


class BookListAPI(Resource):
    def get(self):
        books = Book.query_db(db.session, **request.args)
        return {
            "status_code": 200,
            "status": "success",
            "data": [book.json() for book in books]
        }

    def post(self):
        try:
            json_data = request.get_json(force=True)
            book = Book(name=json_data['name'], isbn=json_data['isbn'], number_of_pages=json_data['number_of_pages'], \
                    publisher=json_data['publisher'], country=json_data['country'], release_date=json_data['release_date'], \
                    authors=json_data["authors"])
            book.create()

            return {
                "status_code": 200,
                "status": "success",
                "data": [
                    {
                        "book": book.json()
                    }
                ]
            }
        except (exc.IntegrityError, ValueError, KeyError) as e:
            db.session().rollback()
            res = BadRequest(e.message)
            res.data = {'message': e.message}
            raise res


class BookExternalAPI(Resource):
    def get(self):
        ice_fire_api = ice_fire_service().get_books(request.args)
        return {
            "status_code": 200,
            "status": "success",
            "data": ice_fire_api
        }
