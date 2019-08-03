import pytest
import json
from pytest import fixture, mark
from mock import Mock
from flask import request
from werkzeug.exceptions import BadRequest

from server import server
from model import Book
from resource.book import BookAPI


class TestBookGetAPI(object):

    def test_get_book(self, monkeypatch):
        book_model = Mock()
        book_model.json.return_value = {'name': 'test book'}

        class MockBook:
            @classmethod
            def find_by_id(klass, id):
                return book_model
        monkeypatch.setattr(Book, "find_by_id", MockBook.find_by_id)

        book = BookAPI().get(1)

        assert book == {'status': 'success',
                        'status_code': 200, 'data': {'name': 'test book'}}

    def test_get_book_invalid_id(self, monkeypatch):
        class MockBook:
            @classmethod
            def find_by_id(klass, id):
                return None
        monkeypatch.setattr(Book, "find_by_id", MockBook.find_by_id)

        book = BookAPI().get(1)

        assert book == {'status': 'success', 'status_code': 200, 'data': {}}


class TestBookPatchAPI(object):

    def test_update_book_invalid_id(self, monkeypatch):
        class MockBook:
            @classmethod
            def find_by_id(klass, id):
                return None
        monkeypatch.setattr(Book, "find_by_id", MockBook.find_by_id)

        with pytest.raises(BadRequest) as ex:
            book = BookAPI().patch(1)

        assert str(ex.value) == '400: Bad Request'

    def test_update_book(self, monkeypatch):
        book_model = Mock()
        book_model.json.return_value = {'name': 'test book'}

        class MockBook:
            @classmethod
            def find_by_id(klass, id):
                return book_model
        monkeypatch.setattr(Book, "find_by_id", MockBook.find_by_id)

        with server.test_request_context('/api/v1/books/1', data=json.dumps({'name': 'new test book'}), method="'PATCH'"):
            book = BookAPI().patch(1)

        book_model.update.assert_called_with({u'name': u'new test book'})
        assert book == {
            "status_code": 200,
            "status": "success",
            "data": {'name': 'test book'}
        }


class TestBookDeleteAPI(object):

    def test_delete_book_invalid_id(self, monkeypatch):
        class MockBook:
            @classmethod
            def find_by_id(klass, id):
                return None
        monkeypatch.setattr(Book, "find_by_id", MockBook.find_by_id)

        with pytest.raises(BadRequest) as ex:
            book = BookAPI().delete(1)

        assert str(ex.value) == '400: Bad Request'

    def test_delete_book(self, monkeypatch):
        book_model = Mock()
        book_model.name = 'test book'

        class MockBook:
            @classmethod
            def find_by_id(klass, id):
                return book_model
        monkeypatch.setattr(Book, "find_by_id", MockBook.find_by_id)

        book = BookAPI().delete(1)

        book_model.delete.assert_called_once()
        assert book == {
            "status_code": 200,
            "status": "success",
            "data": [],
            "message": "The book test book was deleted successfully"
        }
