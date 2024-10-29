FROM python:3.12-alpine

MAINTAINER Kathryn Janzen <kathryn.janzen@lightsource.ca>

COPY requirements.txt /

RUN apk add --no-cache --virtual libpq apache2-ssl apache2-mod-wsgi certbot-apache openssl sed py3-pip imagemagick

RUN set -ex && \
    /usr/bin/python3 -m venv /venv && source /venv/bin/activate && \
    /venv/bin/pip3 install --no-cache-dir --upgrade pip && \
    /venv/bin/pip3 install --no-cache-dir -r /requirements.txt

EXPOSE 443 80

ADD . /website
ADD ./local /website/local

COPY deploy/run-server.sh /
COPY deploy/wait-for-it.sh /
COPY deploy/website.conf /etc/apache2/conf.d/zzzwebsite.conf

RUN chmod -v +x /run-server.sh /wait-for-it.sh
RUN sed -i -E 's@#!/usr/bin/env python@#!/venv/bin/python3@' /website/manage.py
RUN /website/manage.py collectstatic --noinput

CMD /run-server.sh