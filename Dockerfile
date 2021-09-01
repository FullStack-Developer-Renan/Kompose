# Imagem base
FROM python:3.9

COPY . /code/

WORKDIR /code

RUN pip install -r requirements.txt

RUN pip install psycopg2

ENV PYTHONUNBUFFERED=1

