FROM talkincode/toughwlan:pypy
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/toughwlan"]

RUN git clone -b master https://github.com/talkincode/toughwlan.git /opt/toughwlan

# etc link

RUN ln -s /opt/toughwlan/toughengine/toughengine.conf /etc/toughengine.conf

RUN ln -s /opt/toughwlan/deploy/toughengine/etc/supervisord.conf /etc/supervisord.conf

# bin link
RUN ln -s /opt/toughwlan/deploy/toughengine/bin/toughengine /usr/bin/toughengine && chmod +x /usr/bin/toughengine

RUN chmod +x /opt/toughwlan/toughengine/toughctl


# radiusd
EXPOSE 22
EXPOSE 1812/udp
EXPOSE 1813/udp
EXPOSE 1815


ENTRYPOINT ["/usr/bin/toughengine","start"]

