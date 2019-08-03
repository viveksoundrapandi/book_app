from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from flask_validator import ValidateInteger, ValidateISBN


from .abc import db, BaseModel
Base = declarative_base()


class Book(db.Model, BaseModel, Base):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    isbn = db.Column(db.String(120), unique=True)
    authors = relationship(
        "Author",
        secondary="book_author")

    number_of_pages = db.Column(db.Integer)
    publisher = db.Column(db.String(120))
    country = db.Column(db.String(120))
    release_date = db.Column(db.Date)

    def __init__(self, name, isbn, number_of_pages, publisher, country, release_date, authors):
        self._name = name
        self._isbn = isbn
        self._number_of_pages = number_of_pages
        self._publisher = publisher
        self._country = country
        self._release_date = release_date
        self._authors = authors
    @hybrid_property
    def _name(self):
        return self.name
    @_name.setter
    def set_name(self, name):
        self.name = name

    @hybrid_property
    def _isbn(self):
        return self.isbn
    @_isbn.setter
    def set_isbn(self, isbn):
        self.isbn = isbn

    @hybrid_property
    def _number_of_pages(self):
        return self.number_of_pages
    @_number_of_pages.setter
    def set_number_of_pages(self, number_of_pages):
        self.number_of_pages = number_of_pages

    @hybrid_property
    def _publisher(self):
        return self.publisher
    @_publisher.setter
    def set_publisher(self, publisher):
        self.publisher = publisher

    @hybrid_property
    def _country(self):
        return self.country
    @_country.setter
    def set_country(self, country):
        self.country = country

    @hybrid_property
    def _release_date(self):

        return self.release_date.strftime("%Y-%m-%d")
    @_release_date.setter
    def set_release_date(self, release_date):
        release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
        self.release_date = release_date

    @hybrid_property
    def _authors(self):
        return [author.name for author in self.authors]
    @_authors.setter
    def set_authors(self, authors):
        self.authors = []
        for author in authors:
            print Author
            author_obj = Author.query.filter_by(name=author).first()
            if author_obj is None:
                author_obj = Author(name=author)
            self.authors.append(author_obj)


    def update(self, patch_data):
        for attr_name, value in patch_data.iteritems():
            if hasattr(self, attr_name):
                setattr(self, "_{:s}".format(attr_name), value)
    def delete(self):
        self._authors = []
        db.session.add(self)
        db.session.commit()
        db.session.delete(self)
        db.session.commit()
    

    def create(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "name": self._name,
            "isbn": self._isbn,
            "number_of_pages": self._number_of_pages,
            "publisher": self._publisher,
            "country": self._country,
            "release_date": self._release_date,
            "authors": self._authors
        }
    @classmethod
    def find_by_id(klass, id):
        return klass.query.filter_by(id=id).first()

    @classmethod
    def __declare_last__(cls):
        # ValidateISBN(cls.isbn)
        ValidateInteger(Book.number_of_pages)


class Author(db.Model, BaseModel, Base):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    books = relationship(
        "Book",
        secondary="book_author")

    def __init__(self, name):
        self.set_name(name)

    def set_name(self, name):
        self.name = name


class BookAuthorLink(db.Model, BaseModel, Base):
    __tablename__ = 'book_author'
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'author.id'), primary_key=True)
    book = relationship(Book, backref=backref("author_assoc"))
    author = relationship(Author, backref=backref("book_assoc"))
