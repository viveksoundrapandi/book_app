from pytest import fixture, mark
from mock import Mock

import config
from services.ice_fire_api_service import IceFireApiService
from util.http_client import HttpClient


class TestIceFireApiService(object):
    @fixture(autouse=True)
    def http_client_fixture(self):
        http_client = Mock()
        return http_client
    
    def test_empty_response_from_api(self, http_client_fixture):
        http_client_fixture.get.return_value = []

        ice_fire = IceFireApiService(http_client_fixture)

        http_client_fixture.assert_called()
        assert ice_fire.get_books({}) == []

    def test_books_with_extra_attributes(self, http_client_fixture):
        book_external_service_response = [
            {
                "url": "https://www.anapioficeandfire.com/api/books/1",
                "name": "A Game of Thrones",
                "isbn": "978-0553103540",
                "authors": [
                    "George R. R. Martin"
                ],
                "numberOfPages": 694,
                "publisher": "Bantam Books",
                "country": "United States",
                "mediaType": "Hardcover",
                "released": "1996-08-01T00:00:00",
                "characters": [
                    "https://www.anapioficeandfire.com/api/characters/2"
                ],
                "povCharacters": [
                    "https://www.anapioficeandfire.com/api/characters/148"

                ]
            }
        ]
        book_sanitized_response = [{'publisher': 'Bantam Books', 'isbn': '978-0553103540', 'name': 'A Game of Thrones', 'country': 'United States', 'release_date': '1996-08-01', 'number_of_pages': 694, 'authors': ['George R. R. Martin']}]
        http_client_fixture.get.return_value = book_external_service_response

        ice_fire = IceFireApiService(http_client_fixture)
        assert ice_fire.get_books({}) == book_sanitized_response

    def test_books_search_with_params(self, http_client_fixture):
        http_client_fixture.get.return_value = []
        search_param = {"name":"test book"}

        ice_fire = IceFireApiService(http_client_fixture)
        ice_fire.get_books(search_param)

        http_client_fixture.get.assert_called_with('https://www.anapioficeandfire.com/api/books', search_param)

    def test_books_search_with_sanitized_params(self, http_client_fixture, monkeypatch):
        monkeypatch.setattr(config, 'ICEFIRE_API_URL', 'test url')
        http_client_fixture.get.return_value = []
        search_param = {"name":"test book", "author":"vivek"}

        ice_fire = IceFireApiService(http_client_fixture)
        ice_fire.get_books(search_param)

        http_client_fixture.get.assert_called_with('test url', {"name":"test book"})