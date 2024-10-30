FROM python:3.12-alpine

MAINTAINER Kathryn Janzen <kathryn.janzen@lightsource.ca>

COPY requirements.txt /
COPY deploy/run-server.sh /
COPY deploy/wait-for-it.sh /
COPY deploy/website.conf /etc/apache2/conf.d/zzzwebsite.conf

ADD . /website
ADD ./local/__init__.py /website/local/__init__.py

RUN set -ex && \
    apk add --no-cache --virtual libpq apache2-ssl apache2-mod-wsgi \
    certbot-apache openssl bash sed py3-pip imagemagick && \
    /usr/bin/python3 -m venv /venv && source /venv/bin/activate && \
    /venv/bin/pip3 install --no-cache-dir --upgrade pip && \
    /venv/bin/pip3 install --no-cache-dir -r /requirements.txt  && \
    chmod -v +x /run-server.sh /wait-for-it.sh && \
    sed -i -E 's@#!/usr/bin/env python@#!/venv/bin/python3@' /website/manage.py && \
    /website/manage.py collectstatic --noinput


EXPOSE 443 80


CMD /run-server.sh