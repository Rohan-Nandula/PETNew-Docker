# syntax=docker/dockerfile:1

FROM python:3.9.5-alpine3.13

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD [ "python3", "__init__.py"]