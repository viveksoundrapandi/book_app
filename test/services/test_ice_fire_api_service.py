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
        http_client_fixture.get.return_value = [{"name":"test book", "extra_param":"extra", 'publisher': None, 'isbn': None, 'name': 'test book', 'country': None, 'release_date': None, 'number_of_pages': None, 'authors': None}]

        ice_fire = IceFireApiService(http_client_fixture)

        assert ice_fire.get_books({}) == [{'publisher': None, 'isbn': None, 'name': 'test book', 'country': None, 'release_date': None, 'number_of_pages': None, 'authors': None}]

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