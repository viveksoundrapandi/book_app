import requests



class HttpClient(object):
    class Decorator(object):
        @classmethod
        def http_wrap(klass,http_method):
            def inner(*args, **kwargs):
                attempt_number = 0
                while(True):
                    try:
                        # sending get request and saving the response as response object 
                        r = http_method(*args, **kwargs)
                        # extracting data in json format 
                        data = r.json()         
                        return data
                    except requests.exceptions.Timeout:
                        attempt_number += 1
                        klass = kwargs["self"] if kwargs.get("self") else args[0]
                        if(attempt_number > klass._retry_limit):
                            raise requests.exceptions.Timeout
            return inner

    def __init__(self, timeout=10, retry_limit=2):
        self._timeout = timeout
        self._retry_limit = retry_limit
        return super(HttpClient, self).__init__()
    
    

    @Decorator.http_wrap
    def get(self, url, params={}, headers={}):
        response = requests.get(url = url, params = params, timeout=self._timeout) 
        return response
                