from flask import jsonify, request
from flask.ext.restful import Resource
from werkzeug.exceptions import BadRequest
import traceback
from sqlalchemy import exc
from flask_request_validator import (
    PATH,
    JSON,
    Param,
    GET,
    Pattern,
    validate_params
)

from wiring import *
from model.abc import db
from model import Book, Author, BookAuthorLink
from util.validation_catcher import catch_validation_error
from util.validators import RELEASE_DATE, ISBN


class BookAPI(Resource):
    @catch_validation_error
    def get(self, id):
        book = Book.find_by_id(id)
        return {
            "status_code": 200,
            "status": "success",
            "data": {} if book is None else book.json()
        }

    @catch_validation_error
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

    @catch_validation_error
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
    @catch_validation_error
    @validate_params(
        Param('name', GET, str, required=False),
        Param('publisher', GET, str, required=False),
        Param('release_date', GET, str, required=False, rules=[RELEASE_DATE]),
        Param('country', GET, str, required=False)
    )
    def get(self, *args):
        books = Book.query_db(db.session, **request.args)
        return {
            "status_code": 200,
            "status": "success",
            "data": [book.json() for book in books]
        }

    @catch_validation_error
    @validate_params(
        Param('name', JSON, str, required=False),
        Param('publisher', JSON, str, required=False),
        Param('release_date', JSON, str, required=False, rules=[RELEASE_DATE]),
        Param('country', JSON, str, required=False),
        Param('number_of_pages', JSON, int, required=False),
        Param('isbn', JSON, str, required=False, rules=[ISBN]),
    )
    def post(self, *args):
        try:
            json_data = request.get_json(force=True)
            book = Book(name=json_data['name'], isbn=json_data['isbn'], number_of_pages=json_data['number_of_pages'],
                        publisher=json_data['publisher'], country=json_data['country'], release_date=json_data['release_date'],
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
    @catch_validation_error
    @validate_params(
        Param('name', GET, str, required=False)
    )
    def get(self, *args):
        ice_fire_api = ice_fire_service().get_books(request.args)
        return {
            "status_code": 200,
            "status": "success",
            "data": ice_fire_api
        }
