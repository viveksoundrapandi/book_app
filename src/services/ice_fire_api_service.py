import config

class IceFireApiService(object):
    SERVICE_PARAMS_MAP = {
        "name": "name"   
    }
    BOOK_ATTRS = ("name", "isbn", "authors", "number_of_pages", "publisher", "country", "release_date")
    def __init__(self, http_client):
        self._http_client = http_client
        return super(IceFireApiService, self).__init__()
    def get_books(self, params):
        books = self._http_client.get(config.ICEFIRE_API_URL, self._sanitize_params(params))
        return self._get_marshalled_books(books)

    def _sanitize_params(self, params):
        return {self.SERVICE_PARAMS_MAP[param_name]:value for param_name, value in params.iteritems() if self.SERVICE_PARAMS_MAP.get(param_name)}

    def _get_marshalled_books(self, books):
        marshalled_books = []
        for book in books:
            marshalled_books.append({ book_attr:book.get(book_attr) for book_attr in self.BOOK_ATTRS})
        return marshalled_books
