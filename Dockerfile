# syntax=docker/dockerfile:1
FROM python:3.9.5-alpine3.13
ENV PYTHONUNBUFFERED 1
RUN apk add build-base  
WORKDIR /petapp
RUN pip3 install virtualenv
RUN virtualenv /petapp
ADD requirements.txt /petapp/
RUN  python3 -m pip install -r requirements.txt --no-cache-dir
ADD . /petapp/
CMD [ "python3", "petapp.py"]
