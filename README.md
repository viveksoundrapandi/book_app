# BookApp

BookApp is a flask based python application to demonstrate CRUD operations with Book as resource

## Architecture

The application requires two microservices namely:
* book_server - REST application to perform CRUD operations on book resource
* book_db - postgres DB to store the data locally

Both the applications are dockerized. postgres is fetched directly from dockerhub base image and book_db is fetched from python 2.7 base image and dependant libraries are installed(internet is required as libraries are installed from pypi).

book_server runs in port 5000 and the same is exposed outside. Kindly ensure no other process runs in port #5000. Code is copied into the image while building and mounted to /app/books location.


## SetUp

To build from begining:

```
# build the images
docker-compose up --build
# run db migration to setup the DB schema
docker-compose run --rm server python src/manage.py db upgrade
```
The application uses SQLAlchemy library as ORM to talk to the database. The schema is stored in the migrations folder and running an upgrade is required to setup the DB for the first time.

To Run:
```
docker-compose run -d server
```

## Run Tests
To run tests:
```
#Run only tests
docker-compose run --rm server pytest -vvv
#Run tests + coverage
docker-compose run --rm server pytest --cov=src --cov-report html test/
```

## Coverage
Coverage reports are run using pytest and exported as HTML files inside htmlcov/ directory(For easy access)

## Accessing containers
```
docker exec -it book_db_1 psql -Upostgres
docker exec -it book_server_1 bash
```
