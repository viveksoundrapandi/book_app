from pytest import fixture, mark
from mock import Mock

from model import Book
from resource.book import BookAPI

@fixture()
def class_fixture():
    return
@mark.usefixtures("class_fixture")
class TestBookAPI(object):

    
    def test_get_book(self, monkeypatch):
        book_model = Mock()
        book_model.json.return_value = {'name':'test book'}
        class MockBook:
            @classmethod
            def find_by_id(klass, id):
                return book_model
        monkeypatch.setattr(Book, "find_by_id", MockBook.find_by_id)

        book = BookAPI().get(1)

        assert book == {'status': 'success', 'status_code': 200, 'data':{'name':'test book'}}

    def test_get_book_invalid_id(self, monkeypatch):
        class MockBook:
            @classmethod
            def find_by_id(klass, id):
                return None
        monkeypatch.setattr(Book, "find_by_id", MockBook.find_by_id)

        book = BookAPI().get(1)

        assert book == {'status': 'success', 'status_code': 200, 'data':{}}
    
