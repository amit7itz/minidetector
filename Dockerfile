FROM python:3.9.6-slim-buster

ENV DB_URI=''

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y libpq-dev python-dev build-essential

RUN pip install -e .
RUN python setup.py install

ENTRYPOINT python -m minidetector.main
