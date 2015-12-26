FROM talkincode/tough-pypy:latest
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/toughwlan"]

RUN pypy -m pip install https://github.com/talkincode/toughlib/archive/master.zip --upgrade --no-deps

RUN git clone -b master https://github.com/talkincode/toughwlan.git /opt/toughwlan

RUN ln -s /opt/toughwlan/toughwlan.conf /etc/toughwlan.conf

RUN chmod +x /opt/toughwlan/toughctl

EXPOSE 1810

CMD ["pypy", "/opt/toughwlan/toughctl", "--admin"]

