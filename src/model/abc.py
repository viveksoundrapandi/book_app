"""Define an Abstract Base Class (ABC) for models."""
import datetime
from weakref import WeakValueDictionary
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.orm import aliased


db = SQLAlchemy()


class MetaBaseModel(db.Model.__class__):
    """ Define a metaclass for the BaseModel to implement `__getitem__` for managing aliases """

    def __init__(cls, *args):
        super().__init__(*args)
        cls.aliases = WeakValueDictionary()

    def __getitem__(cls, key):
        try:
            alias = cls.aliases[key]
        except KeyError:
            alias = aliased(cls)
            cls.aliases[key] = alias
        return alias


class BaseModel():
    """ Generalize __init__, __repr__
        Based on the models columns """

    print_filter = ()

    def __repr__(self):
        """ Define a base way to print models
            Columns inside `print_filter` are excluded """
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self.__dict__.items()
            if column not in self.print_filter
        })

    @classmethod
    def query_db(klass, session, **kwargs):
        q = session.query(klass)
        for k, v in kwargs.items():
            if hasattr(klass, k):
                q = q.filter(getattr(klass, k).in_(v))
        return q
