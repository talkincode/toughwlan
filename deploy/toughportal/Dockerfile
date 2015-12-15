FROM talkincode/toughwlan:pypy
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/toughwlan"]

RUN git clone -b master https://github.com/talkincode/toughwlan.git /opt/toughwlan

# etc link

RUN ln -s /opt/toughwlan/toughportal/toughportal.conf /etc/toughportal.conf

RUN ln -s /opt/toughwlan/deploy/toughportal/etc/supervisord.conf /etc/supervisord.conf

# nginx config link

RUN rm -f /etc/nginx/nginx.conf
RUN ln -s /opt/toughwlan/deploy/toughportal/etc/nginx.conf /etc/nginx/nginx.conf
RUN ln -s /opt/toughwlan/deploy/toughportal/etc/toughportal-nginx.conf /etc/nginx/conf.d/toughportal-nginx.conf

# bin link
RUN ln -s /opt/toughwlan/deploy/toughportal/bin/toughportal /usr/bin/toughportal && chmod +x /usr/bin/toughportal

RUN chmod +x /opt/toughwlan/toughportal/toughctl

# portal
EXPOSE 1818
EXPOSE 50100/udp

ENTRYPOINT ["/usr/bin/toughportal","start"]

