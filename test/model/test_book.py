from pytest import fixture, mark
from mock import Mock
from flask import Flask
from model.abc import db

import config
from model.book import Book, Author
server = Flask(__name__)
server.debug = config.DEBUG
server.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
db.init_app(server)
db.app = server

@fixture()
def class_fixture():
    return
@mark.usefixtures("class_fixture")
class TestBook(object):
    @fixture(autouse=True)
    def book_fixture(self):
        return {
            "name":"GOT",
            "isbn":"1",
            "authors":["vivek"],
            "number_of_pages": 3,
            "publisher": "RR Martin",
            "country": "UK",
            "release_date": "2017-10-12",
        }
    
    def test_return_book_as_json_serializable(self, book_fixture):
        book = Book(**book_fixture)

        assert book.json() == {'publisher': 'RR Martin', 'isbn': '1', 'name': 'GOT', 'authors': [u'vivek'], 'country': 'UK', 'release_date': '2017-10-12', 'number_of_pages': 3, 'id': None}
    
    def test_update_book_for_0_params(self, book_fixture):
        book = Book(**book_fixture)

        book.update({})

        assert book.json() == {'publisher': 'RR Martin', 'isbn': '1', 'name': 'GOT', 'authors': [u'vivek'], 'country': 'UK', 'release_date': '2017-10-12', 'number_of_pages': 3, 'id': None}

    def test_update_book_for_multiple_params(self, book_fixture):
        book = Book(**book_fixture)

        book.update({"name":"Game of Thrones", "isbn":"11"})

        assert book.json() == {'publisher': 'RR Martin', 'isbn': '11', 'name': 'Game of Thrones', 'authors': [u'vivek'], 'country': 'UK', 'release_date': '2017-10-12', 'number_of_pages': 3, 'id': None}

    def test_update_book_for_author(self, book_fixture, monkeypatch):
        book = Book(**book_fixture)

        book.update({"authors":["G. RR Martin"]})

        assert book.json() == {'publisher': 'RR Martin', 'isbn': '1', 'name': 'GOT', 'authors': ['G. RR Martin'], 'country': 'UK', 'release_date': '2017-10-12', 'number_of_pages': 3, 'id': None}

    def test_find_book_by_id(self, book_fixture, monkeypatch):
        book = Book(**book_fixture)

        Book.find_by_id(43)

        assert book.json() == {'publisher': 'RR Martin', 'isbn': '1', 'name': 'GOT', 'authors': [u'vivek'], 'country': 'UK', 'release_date': '2017-10-12', 'number_of_pages': 3, 'id': None}

    # def test_delete(self, book_fixture, monkeypatch):
    #     book = Book(**book_fixture)
    #     book.delete()
    
    # def test_create(self, book_fixture, monkeypatch):
    #     book = Book(**book_fixture)
    #     book.create()
