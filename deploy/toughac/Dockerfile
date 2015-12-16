FROM talkincode/toughwlan:pypy
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/toughwlan"]

RUN git clone -b master https://github.com/talkincode/toughwlan.git /opt/toughwlan

# etc link

RUN ln -s /opt/toughwlan/toughac/toughac.conf /etc/toughac.conf
RUN ln -s /opt/toughwlan/deploy/toughac/etc/supervisord.conf /etc/supervisord.conf

# bin link
RUN ln -s /opt/toughwlan/deploy/toughac/bin/toughac /usr/bin/toughac && chmod +x /usr/bin/toughac

RUN chmod +x /opt/toughwlan/toughac/toughctl

# ac
EXPOSE 22
EXPOSE 1819
EXPOSE 2000/udp
EXPOSE 3799/udp

ENTRYPOINT ["/usr/bin/toughac","start"]

