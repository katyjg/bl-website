FROM python:3.7-alpine

MAINTAINER Kathryn Janzen <kathryn.janzen@lightsource.ca>

COPY requirements.txt /

RUN apk add --no-cache --virtual .build-deps bash gcc linux-headers musl-dev postgresql-dev libpq libffi-dev \
    jpeg-dev zlib-dev apache2-ssl apache2-mod-wsgi certbot-apache openssl openssl-dev python3-dev imagemagick

RUN set -ex && /usr/bin/pip3 install --upgrade pip && /usr/bin/pip3 install --no-cache-dir -r /requirements.txt

EXPOSE 443

ADD . /website
ADD ./local /website/local

COPY deploy/run-server.sh /
COPY deploy/wait-for-it.sh /
COPY deploy/website.conf /etc/apache2/conf.d/zzzwebsite.conf

RUN chmod -v +x /run-server.sh /wait-for-it.sh
RUN /usr/bin/python3 website/manage.py collectstatic --noinput

CMD /run-server.sh