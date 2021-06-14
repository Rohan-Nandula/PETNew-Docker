FROM alpine:latest

RUN apk add --no-cache sudo git python3-dev uwsgi py-pip uwsgi-router_uwsgi uwsgi-python openssh && \
	pip3 install --updgrade pip && \
    rm -rf /var/cache/apk/*

RUN pip3 --no-cache-dir install -r requirements.txt

RUN mkdir -p /app/pet && \
    adduser -D -s /bin/sh -h /app pet

COPY run.sh /app

COPY uwsgi.ini /app/uwsgi.ini

COPY pet /app/pet

RUN chown -R pet:pet /app

VOLUME ["/app/pet"]

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["run.sh"]