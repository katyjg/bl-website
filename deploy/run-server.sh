#!/bin/bash

# Make sure we're not confused by old, incompletely-shutdown httpd
# context after restarting the container.  httpd won't start correctly
# if it thinks it is already running.
rm -rf /run/httpd/* /tmp/httpd*

# check of database exists and initialize it if not
if [ ! -d /website/static ]; then
    su -s /bin/bash apache -c "/website/manage.py syncdb --noinput"
    su -s /bin/bash apache -c "/website/manage.py collectstatic --noinput"
fi

exec /usr/sbin/httpd -D FOREGROUND
