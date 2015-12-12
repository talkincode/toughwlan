FROM index.alauda.cn/toughstruct/tough-pypy
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/toughportal"]

RUN git clone -b master https://jamiesun@bitbucket.org/talkincode/toughwlan-portal.git /opt/toughportal
RUN ln -s /opt/toughportal/toughctl /usr/bin/toughctl && chmod +x /usr/bin/toughctl
RUN ln -s /opt/toughportal/etc/toughportal.conf /etc/toughportal.conf
RUN ln -s /opt/toughportal/etc/supervisord.conf /etc/supervisord.conf
RUN ln -s /opt/toughportal/etc/toughportal /usr/bin/toughportal && chmod +x /usr/bin/toughportal
RUN rm -f /etc/nginx/nginx.conf && ln -s /opt/toughportal/etc/nginx.conf /etc/nginx/nginx.conf
RUN ln -s /opt/toughportal/etc/toughportal-nginx.conf /etc/nginx/conf.d/toughportal-nginx.conf


EXPOSE 1818
EXPOSE 50100/udp

ENTRYPOINT ["/usr/bin/toughportal","start"]

