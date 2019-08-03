FROM python:2.7
RUN apt-get update

ENV APP_HOME /app/books
ADD . $APP_HOME
WORKDIR $APP_HOME
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# RUN python src/manage.py db init
# RUN python src/manage.py db migrate
# RUN python src/manage.py db upgrade