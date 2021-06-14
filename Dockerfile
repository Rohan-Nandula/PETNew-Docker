FROM alpine:3.4

RUN apk add --no-cache sudo git python uwsgi py-pip uwsgi-router_uwsgi uwsgi-python openssh && \
    rm -rf /var/cache/apk/*

RUN pip install paste flask flask_login sqlalchemy flask_sqlalchemy flask_login requests PyJWT passlib python-dotenv shortuuid Flask-JWT-Extended werkzeug

RUN mkdir -p /app/pet && \
    adduser -D -s /bin/sh -h /app www

COPY run.sh /app
COPY uwsgi.ini /app/uwsgi.ini

RUN chown -R pet:pet /app

VOLUME ["/app/pet"]

ENTRYPOINT ["/app/run.sh"]