FROM talkincode/tough-pypy:latest
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/toughportal"]

RUN git clone -b master https://github.com/talkincode/toughportal.git /opt/toughportal

# etc link

RUN ln -s /opt/toughportal/toughportal.conf /etc/toughportal.conf

RUN ln -s /opt/toughportal/etc/supervisord.conf /etc/supervisord.conf

# nginx config link

RUN rm -f /etc/nginx/nginx.conf
RUN ln -s /opt/toughportal/etc/nginx.conf /etc/nginx/nginx.conf
RUN ln -s /opt/toughportal/etc/toughportal-nginx.conf /etc/nginx/conf.d/toughportal-nginx.conf

# bin link
RUN ln -s /opt/toughportal/bin/toughportal /usr/bin/toughportal && chmod +x /usr/bin/toughportal

RUN chmod +x /opt/toughportal/toughctl

# portal
EXPOSE 22
EXPOSE 1818
EXPOSE 50100/udp

ENTRYPOINT ["/usr/bin/toughportal","start"]

