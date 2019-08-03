import pytest
from pytest import fixture, mark
from mock import Mock
import json
from werkzeug.exceptions import BadRequest
from sqlalchemy import exc


from model import Book
from server import server
from resource.book import BookListAPI


class TestBookListGetAPI(object):

    def test_get_all_books(self, monkeypatch):
        book_model = Mock()
        book_model.json.return_value = {'name': 'test book 1'}
        book_model2 = Mock()
        book_model2.json.return_value = {'name': 'test book 2'}

        class MockBook:
            @classmethod
            def query_db(self, session, **kwargs):
                return [book_model, book_model2]
        monkeypatch.setattr(Book, "query_db", MockBook.query_db)

        with server.test_request_context('/api/v1/books/', data=json.dumps({}), method="'GET'"):
            book = BookListAPI().get()

        assert book == {
            "status_code": 200,
            "status": "success",
            "data": [{'name': 'test book 1'}, {'name': 'test book 2'}]
        }

    def test_get_books_by_attribute(self, monkeypatch):
        book_model = Mock()
        book_model.json.return_value = {'name': 'test book 1'}
        book_model2 = Mock()
        book_model2.json.return_value = {'name': 'test book 2'}

        class MockBook:
            @classmethod
            def query_db(self, session, **kwargs):
                return [book_model, book_model2]
        monkeypatch.setattr(Book, "query_db", MockBook.query_db)

        with server.test_request_context('/api/v1/books/', data=json.dumps({'name': 'test'}), method="'GET'"):
            book = BookListAPI().get()

        assert book == {
            "status_code": 200,
            "status": "success",
            "data": [{'name': 'test book 1'}, {'name': 'test book 2'}]
        }

    def test_get_all_books_no_result(self, monkeypatch):
        class MockBook:
            @classmethod
            def query_db(self, session, **kwargs):
                return []
        monkeypatch.setattr(Book, "query_db", MockBook.query_db)

        with server.test_request_context('/api/v1/books/', data=json.dumps({}), method="'GET'"):
            book = BookListAPI().get()

        assert book == {
            "status_code": 200,
            "status": "success",
            "data": []
        }


class TestBookListCreateAPI(object):

    def test_create_new_book(self, monkeypatch):
        reuqest_data = {
            "name": "node",
            "isbn": "22",
            "number_of_pages": 3,
            "publisher": "devs",
            "country": "IN",
            "release_date": "2018-10-11",
            "authors": ["vivek"]

        }

        class MockBook:
            @classmethod
            def create(self):
                return None
        monkeypatch.setattr(Book, "create", MockBook.create)

        with server.test_request_context('/api/v1/books/', data=json.dumps(reuqest_data), method="'POST'"):
            book = BookListAPI().post()

        reuqest_data["id"] = None
        assert book == {
            "status_code": 200,
            "status": "success",
            "data": [
                {
                    "book": reuqest_data
                }
            ]
        }

    def test_create_invalid_book(self, monkeypatch):
        reuqest_data = {
            "name": "node",
            "number_of_pages": 3,
            "publisher": "devs",
            "country": "IN",
            "release_date": "2018-10-11",
            "authors": ["vivek"]

        }

        class MockBook:
            @classmethod
            def create(self):
                return None
        monkeypatch.setattr(Book, "create", MockBook.create)

        with server.test_request_context('/api/v1/books/', data=json.dumps(reuqest_data), method="'POST'"):
            with pytest.raises(BadRequest) as ex:
                book = BookListAPI().post()
            assert str(ex.value) == '400: Bad Request'

    def test_create_dulpicate_entry(self, monkeypatch):
        reuqest_data = {
            "name": "node",
            "isbn": "duplicate_isbn",
            "number_of_pages": 3,
            "publisher": "devs",
            "country": "IN",
            "release_date": "2018-10-11",
            "authors": ["vivek"]

        }
        class MockBook:
            @classmethod
            def create(self):
                raise exc.IntegrityError("", "", "", "")
        monkeypatch.setattr(Book, "create", MockBook.create)

        with server.test_request_context('/api/v1/books/', data=json.dumps(reuqest_data), method="'POST'"):
            with pytest.raises(BadRequest) as ex:
                book = BookListAPI().post()
            assert str(ex.value) == '400: Bad Request'
