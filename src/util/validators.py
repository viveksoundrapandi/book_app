from flask_request_validator import (
    PATH,
    JSON,
    Param,
    GET,
    Pattern,
    validate_params
)
RELEASE_DATE = Pattern(
    r'(?:[0-9]{4}-([0-1]{1})([0-9]{1})-([0-3]{1})([0-9]{1}))')
ISBN = Pattern(r'ISBN\x20(?=.{13}$)\d{1,5}([- ])\d{1,7}\1\d{1,6}\1(\d|X)$')
