FROM talkincode/pypy:latest
MAINTAINER jamiesun <jamiesun.net@gmail.com>


ADD etc/toughengine.conf /etc/toughengine.conf
ADD etc/supervisord.conf /etc/supervisord.conf
ADD bin/trengine /usr/bin/trengine

RUN chmod +x /usr/bin/trengine

RUN pypy -m  pip install supervisor
RUN pypy -m  pip install Mako==0.9.0
RUN pypy -m  pip install Beaker==1.6.4
RUN pypy -m  pip install MarkupSafe==0.18
RUN pypy -m  pip install Twisted
RUN pypy -m  pip install treq
RUN pypy -m  pip install cyclone
RUN pypy -m  pip install six
RUN pypy -m  pip install autobahn
RUN pypy -m  pip install pycrypto
RUN pypy -m  pip install pyOpenSSL>=0.14
RUN pypy -m  pip install service_identity

RUN git clone -b master https://github.com/talkincode/toughengine.git /opt/toughengine
RUN ln -s /opt/toughengine/toughctl /usr/bin/toughctl && chmod +x /usr/bin/toughctl

EXPOSE 1815
EXPOSE 1812/udp
EXPOSE 1813/udp

VOLUME [ "/var/toughengine" ]
ENTRYPOINT ["/usr/bin/trengine","start"]

