FROM python:3.7-alpine

MAINTAINER Kathryn Janzen <kathryn.janzen@lightsource.ca>

COPY requirements.txt /

RUN apk add --no-cache --virtual .build-deps bash gcc linux-headers musl-dev postgresql-dev libpq libffi-dev \
    jpeg-dev zlib-dev apache2-ssl apache2-mod-wsgi certbot-apache openssl openssl-dev python3-dev

#RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
#RUN pip install -r /requirements.txt
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


## vvv Dockerfile created with wagtail vvv #
## Use an official Python runtime as a parent image
#FROM python:3.7
#LABEL maintainer="hello@wagtail.io"
#
## Set environment varibles
#ENV PYTHONUNBUFFERED 1
#ENV DJANGO_ENV dev
#
#COPY ./requirements.txt /code/requirements.txt
#RUN pip install --upgrade pip
## Install any needed packages specified in requirements.txt
#RUN pip install -r /code/requirements.txt
#RUN pip install gunicorn
#
## Copy the current directory contents into the container at /code/
#COPY . /code/
## Set the working directory to /code/
#WORKDIR /code/
#
#RUN python manage.py migrate
#
#RUN useradd wagtail
#RUN chown -R wagtail /code
#USER wagtail
#
#EXPOSE 8000
#CMD exec gunicorn beamol.wsgi:application --bind 0.0.0.0:8000 --workers 3
