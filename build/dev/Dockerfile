FROM daocloud.io/toughcloud/docker-base
MAINTAINER toughcloud <support@toughstruct.com>

VOLUME ["/var/toughwlan"]

RUN pypy -m pip install Click
RUN pypy -m pip install https://github.com/talkincode/toughlib/archive/master.zip --upgrade --no-deps
RUN pypy -m pip install https://github.com/talkincode/txportal/archive/master.zip --upgrade --no-deps
RUN git clone -b release-dev https://github.com/talkincode/toughwlan.git /opt/toughwlan && \
    ln -s /opt/toughwlan/etc/toughwlan.json /etc/toughwlan.json && \
    chmod +x /opt/toughwlan/wlanctl 

ADD entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 1810
EXPOSE 50100/udp

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["python", "/opt/toughwlan/wlanctl", "standalone]"

