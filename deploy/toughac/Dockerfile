FROM talincode/toughwlan-pypy
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/tougwlan/acagent"]

RUN git clone -b master https://jamiesun@bitbucket.org/talkincode/toughwlan-portal.git /opt/toughwlan/acagent
RUN chmod +x /opt/toughwlan/acagent/toughctl /usr/bin/toughctl
RUN ln -s /opt/toughwlan/acagent/etc/toughac.conf /etc/toughac.conf
RUN ln -s /opt/toughwlan/acagent/etc/supervisord.conf /etc/supervisord.conf
RUN ln -s /opt/toughwlan/acagent/etc/toughac /usr/bin/toughac && chmod +x /usr/bin/toughac
RUN rm -f /etc/nginx/nginx.conf && ln -s /opt/toughwlan/acagent/etc/nginx.conf /etc/nginx/nginx.conf
RUN ln -s /opt/toughwlan/acagent/etc/toughac-nginx.conf /etc/nginx/conf.d/toughac-nginx.conf


EXPOSE 8088
EXPOSE 2000/udp
EXPOSE 3799/udp


ENTRYPOINT ["/usr/bin/toughac","start"]

