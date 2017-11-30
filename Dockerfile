FROM fedora:26
MAINTAINER Kathryn Janzen <kathryn.janzen@lightsource.ca>

RUN dnf -y update
RUN dnf -y install httpd python-django mod_wsgi python-ipaddr python-pillow  python-dateutil python-markdown python-unicodecsv && dnf clean all
RUN dnf -y install python-psycopg2 && dnf clean all

RUN pip install --upgrade pip &&  pip install 'Django==1.11'

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

