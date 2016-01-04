FROM talkincode/tough-pypy:latest
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/toughwlan"]

RUN pypy -m pip install https://github.com/talkincode/toughlib/archive/master.zip --upgrade --no-deps
RUN pypy -m pip install https://github.com/talkincode/txportal/archive/master.zip --upgrade --no-deps
RUN pypy -m pip install https://github.com/talkincode/txradius/archive/master.zip --upgrade --no-deps

RUN git clone -b master https://github.com/talkincode/toughwlan.git /opt/toughwlan

RUN ln -s /opt/toughwlan/toughwlan.json /etc/toughwlan.json

RUN chmod +x /opt/toughwlan/toughctl

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

CMD ["pypy", "/opt/toughwlan/toughctl", "--standalone"]

