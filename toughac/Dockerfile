FROM talkincode/tough-pypy:latest
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/tougac"]

RUN git clone -b master https://github.com/talkincode/toughac.git /opt/toughac

# etc link

RUN ln -s /opt/toughac/toughac/toughac.conf /etc/toughac.conf
RUN ln -s /opt/toughac/etc/supervisord.conf /etc/supervisord.conf

# bin link
RUN ln -s /opt/toughac/bin/toughac /usr/bin/toughac && chmod +x /usr/bin/toughac

RUN chmod +x /opt/toughac/toughctl

# ac
EXPOSE 22
EXPOSE 1819
EXPOSE 2000/udp
EXPOSE 3799/udp

ENTRYPOINT ["/usr/bin/toughac","start"]

