FROM index.alauda.cn/toughstruct/tough-pypy:twlan
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/toughwlan"]

RUN pypy -m pip install https://github.com/talkincode/toughlib/archive/master.zip --upgrade --no-deps
RUN pypy -m pip install https://github.com/talkincode/txportal/archive/master.zip --upgrade --no-deps
RUN git clone -b master https://github.com/talkincode/toughwlan.git /opt/toughwlan && \
    ln -s /opt/toughwlan/toughwlan.json /etc/toughwlan.json && \
    chmod +x /opt/toughwlan/toughctl 

ADD scripts/initdb /usr/local/bin/initdb
RUN chmod +x /usr/local/bin/initdb

ADD entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 1810
EXPOSE 50100/udp

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["pypy", "/opt/toughwlan/toughctl", "--standalone]"
