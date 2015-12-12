FROM talkincode/toughwlan:pypy
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/toughwlan"]

RUN git clone -b master https://github.com/talkincode/toughwlan.git /opt/toughwlan

#etc

RUN ln -s /opt/toughwlan/toughac/toughac.conf /etc/toughac.conf
RUN ln -s /opt/toughwlan/toughadmin/toughadmin.conf /etc/toughadmin.conf
RUN ln -s /opt/toughwlan/toughportal/toughportal.conf /etc/toughportal.conf
RUN ln -s /opt/toughwlan/toughengine/toughengine.conf /etc/toughengine.conf

RUN ln -s /opt/toughwlan/standalone/etc/supervisord.conf /etc/supervisord.conf

#nginx

RUN rm -f /etc/nginx/nginx.conf
RUN ln -s /opt/toughwlan/standalone/etc/nginx.conf /etc/nginx/nginx.conf
RUN ln -s /opt/toughwlan/standalone/etc/toughadmin-nginx.conf /etc/nginx/conf.d/toughadmin-nginx.conf
RUN ln -s /opt/toughwlan/standalone/etc/toughportal-nginx.conf /etc/nginx/conf.d/toughportal-nginx.conf

#bin

RUN ln -s /opt/toughwlan/standalone/bin/toughwlan /usr/bin/toughwlan && chmod +x /usr/bin/toughwlan

RUN chmod +x /opt/toughwlan/toughac/toughctl
RUN chmod +x /opt/toughwlan/toughadmin/toughctl
RUN chmod +x /opt/toughwlan/toughportal/toughctl
RUN chmod +x /opt/toughwlan/toughengine/toughctl

#admin
EXPOSE 1810

#ac
EXPOSE 8088
EXPOSE 2000/udp
EXPOSE 3799/udp

#radiusd
EXPOSE 1812/udp
EXPOSE 1813/udp

#portal
EXPOSE 1818
EXPOSE 50100/udp

ENTRYPOINT ["/usr/bin/toughwlan","start"]

