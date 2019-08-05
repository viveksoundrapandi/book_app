from datetime import datetime
import config


class IceFireApiService(object):
    SERVICE_PARAMS_MAP = {
        "name": "name",
    }
    

    def __init__(self, http_client):
        self.BOOK_ATTRS = {"name": ("name", self._format_none),
                  "isbn": ("isbn", self._format_none),
                  "authors": ("authors", self._format_none),
                  "number_of_pages": ("numberOfPages", self._format_none),
                  "publisher": ("publisher", self._format_none),
                  "country": ("country", self._format_none),
                  "release_date": ("released", self._format_date)
                  }
        self._http_client = http_client
        return super(IceFireApiService, self).__init__()

    def get_books(self, params):
        books = self._http_client.get(
            config.ICEFIRE_API_URL, self._sanitize_params(params))
        return self._get_marshalled_books(books)

    def _sanitize_params(self, params):
        return {self.SERVICE_PARAMS_MAP[param_name]: value for param_name, value in params.iteritems() if self.SERVICE_PARAMS_MAP.get(param_name)}

    def _get_marshalled_books(self, books):
        marshalled_books = []
        for book in books:
            marshalled_books.append({internal_attr_name: book_formatters[1](book.get(
                book_formatters[0])) for internal_attr_name, book_formatters in self.BOOK_ATTRS.iteritems()})
        return marshalled_books

    def _format_none(self, data):
        return data

    def _format_date(self, date):
        return datetime.strptime(date, "%Y-%m-%dT00:00:00").strftime("%Y-%m-%d")
