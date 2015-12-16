FROM talkincode/toughwlan:pypy
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/toughwlan"]

RUN git clone -b master https://github.com/talkincode/toughwlan.git /opt/toughwlan

# etc link

RUN ln -s /opt/toughwlan/toughadmin/toughadmin.conf /etc/toughadmin.conf
RUN ln -s /opt/toughwlan/deploy/toughadmin/etc/supervisord.conf /etc/supervisord.conf

# nginx config link

RUN rm -f /etc/nginx/nginx.conf
RUN ln -s /opt/toughwlan/deploy/toughadmin/etc/nginx.conf /etc/nginx/nginx.conf
RUN ln -s /opt/toughwlan/deploy/toughadmin/etc/toughadmin-nginx.conf /etc/nginx/conf.d/toughadmin-nginx.conf

# bin link
RUN ln -s /opt/toughwlan/deploy/toughadmin/bin/toughadmin /usr/bin/toughadmin && chmod +x /usr/bin/toughadmin

RUN chmod +x /opt/toughwlan/toughadmin/toughctl


# admin
EXPOSE 22
EXPOSE 1810

ENTRYPOINT ["/usr/bin/toughadmin","start"]

