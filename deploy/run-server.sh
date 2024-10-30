#!/usr/bin/env bash

export SERVER_NAME=${SERVER_NAME:-$(hostname --fqdn)}
export CERT_PATH=${CERT_PATH:-/etc/letsencrypt/live/${SERVER_NAME}}

CERT_KEY=${CERT_PATH}/privkey.pem
if [ ! -f $CERT_KEY ]; then
    openssl req -x509 -nodes -newkey rsa:2048 -keyout ${CERT_KEY} -out ${CERT_PATH}/fullchain.pem -subj '/CN=${SERVER_NAME}'
fi

# Make sure we're not confused by old, incompletely-shutdown httpd
# context after restarting the container.  httpd won't start correctly
# if it thinks it is already running.
rm -rf /run/httpd/* /tmp/httpd*

# Wait for the database to be ready
/wait-for-it.sh database:5432 -t 60 &&

# Make sure the local directory is a Python package
if [ ! -f /website/local/__init__.py ]; then
    touch /website/local/__init__.py
fi

# Initialize database and adjust media directory permissions
if [ ! -f /website/local/.dbinit ]; then
    for try in {1..5}; do
        /website/manage.py migrate --noinput &&
        chown -R apache:apache /website/local/media &&
        touch /website/local/.dbinit &&
        break
        sleep 5
    done
else
    for try in {1..5}; do
        /website/manage.py migrate --noinput && break
        sleep 5
    done
fi

# Launch the server
exec /usr/sbin/httpd -DFOREGROUND -e debug
