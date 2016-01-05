FROM talkincode/tough-pypy:kiss
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/toughwlan"]

ADD toughrun /usr/local/bin/toughrun
RUN chmod +x /usr/local/bin/toughrun
RUN /usr/local/bin/toughrun install

# admin web port
EXPOSE 1810

# portal web port
EXPOSE 1818

# ac auth web port
EXPOSE 1819

# ac portal port
EXPOSE 2000/udp

# ac radius port
EXPOSE 3799/udp

# portal listen port
EXPOSE 50100/udp

CMD ["/usr/local/bin/toughrun", "standalone"]

