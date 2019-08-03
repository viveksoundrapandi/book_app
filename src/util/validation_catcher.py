from werkzeug.exceptions import BadRequest
from flask_request_validator.exceptions import InvalidRequest
from sqlalchemy.exc import DataError, InvalidRequestError


def catch_validation_error(func):

    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (DataError, InvalidRequest, InvalidRequestError) as e:
            res = BadRequest(e.message)
            res.data = {'message': e.message}
            raise res
    return func_wrapper
