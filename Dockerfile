FROM python:2.7
RUN apt-get update

ENV APP_HOME /app/books
COPY . $APP_HOME
ADD . $APP_HOME
WORKDIR $APP_HOME
RUN pip install --upgrade pip

RUN pip install -r requirements.txt