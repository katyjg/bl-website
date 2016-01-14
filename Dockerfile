FROM fedora:22
MAINTAINER Michel Fodje <michel.fodje@lightsource.ca>

RUN dnf -y update && dnf clean all
RUN dnf -y install httpd python-django mod_wsgi python-ipaddr python-pillow  python-dateutil python-markdown && dnf clean all
RUN dnf -y install MySQL-python && dnf clean all

EXPOSE 80

# Simple startup script to avoid some issues observed with container restart 
ADD . /website
ADD ./local /website/local
ADD deploy/run-server.sh /run-server.sh
RUN chmod -v +x /run-server.sh
RUN /bin/cp /website/deploy/website.conf /etc/httpd/conf.d/
RUN /website/manage.py collectstatic --noinput

VOLUME ["/website/local"]

CMD ["/run-server.sh"]

