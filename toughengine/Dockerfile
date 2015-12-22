FROM talkincode/tough-pypy:latest
MAINTAINER jamiesun <jamiesun.net@gmail.com>

RUN git clone -b master https://github.com/talkincode/toughengine.git /opt/toughengine
RUN chmod +x /opt/toughengine/toughctl
RUN ln -s /opt/toughengine/bin/trengine /usr/bin/trengine && chmod +x /usr/bin/trengine
RUN ln -s /opt/toughengine/etc/toughengine.conf /etc/toughengine.conf
RUN ln -s /opt/toughengine/etc/supervisord.conf /etc/supervisord.conf

EXPOSE 1815
EXPOSE 10322
EXPOSE 1812/udp
EXPOSE 1813/udp

VOLUME [ "/var/toughengine" ]
ENTRYPOINT ["/usr/bin/trengine","start"]

