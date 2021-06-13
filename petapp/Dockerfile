# syntax=docker/dockerfile:1
FROM python:3.9.5-alpine3.13
ENV PYTHONUNBUFFERED 1
apk add build-base   
WORKDIR /app
RUN pip3 install virtualenv
RUN virtualenv /app
ADD requirements.txt /app/
RUN  python3 -m pip install -r requirements.txt --no-cache-dir
ADD . /app/
CMD [ "flask", "run"]
