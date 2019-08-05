from pytest import fixture, mark
from mock import Mock
import json
from server import server

from resource.book import BookExternalAPI
import wiring
from services.ice_fire_api_service import IceFireApiService


class TestBookAPI(object):

    def test_get_external_book(self, monkeypatch):
        book_sanitized_response = {
            "status_code": 200,
            "status": "success",
            "data": [
                {
                    "name": "A Game of Thrones",
                    "isbn": "978-0553103540",
                    "authors": [
                        "George R. R. Martin"
                    ],
                    "number_of_pages": 694,
                    "publisher": "Bantam Books",
                    "country": "United States",
                    "release_date": "1996-08-01"
                },
                {
                    "name": "A Clash of Kings",
                    "isbn": "978-0553108033",
                    "authors": [
                        "George R. R. Martin"
                    ],
                    "number_of_pages": 768,
                    "publisher": "Bantam Books",
                    "country": "United States",
                    "release_date": "1999-02-02"
                }
            ]
        }
        
        ice_fire_service = Mock()
        ice_fire_service.return_value = book_sanitized_response
        monkeypatch.setattr(IceFireApiService, "get_books", ice_fire_service)
        with server.test_request_context('/api/external-books?name=A Game of Thrones', data=json.dumps({}), method="'GET'"):
            book = BookExternalAPI().get()
        assert book == {'status': 'success',
                        'status_code': 200, 'data': book_sanitized_response}

    def test_get_external_book_empty_response(self, monkeypatch):
        book_sanitized_response = []
        
        ice_fire_service = Mock()
        ice_fire_service.return_value = book_sanitized_response
        monkeypatch.setattr(IceFireApiService, "get_books", ice_fire_service)
        with server.test_request_context('/api/external-books?name=A Game of Thrones', data=json.dumps({}), method="'GET'"):
            book = BookExternalAPI().get()
        assert book == {'status': 'success',
                        'status_code': 200, 'data': []}
