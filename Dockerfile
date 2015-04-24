FROM fedora:21
MAINTAINER Michel Fodje <michel.fodje@lightsource.ca>

RUN yum -y update && yum clean all
RUN yum -y install httpd python-django mod_wsgi python-ipaddr python-pillow  python-dateutil python-markdown && yum clean all

EXPOSE 80

# Simple startup script to avoid some issues observed with container restart 
ADD . /website
ADD deploy/run-server.sh /run-server.sh
RUN chmod -v +x /run-server.sh
RUN /bin/cp /website/deploy/website.conf /etc/httpd/conf.d/

VOLUME ["/website/local"]

CMD ["/run-server.sh"]

