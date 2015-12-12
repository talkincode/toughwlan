FROM index.alauda.cn/toughstruct/tough-pypy
MAINTAINER jamiesun <jamiesun.net@gmail.com>

VOLUME ["/var/toughadmin"]

RUN git clone -b master https://jamiesun@bitbucket.org/talkincode/toughwlan-admin.git /opt/toughadmin
RUN ln -s /opt/toughadmin/toughctl /usr/bin/toughctl && chmod +x /usr/bin/toughctl
RUN ln -s /opt/toughadmin/etc/toughadmin.conf /etc/toughadmin.conf
RUN ln -s /opt/toughadmin/etc/supervisord.conf /etc/supervisord.conf
RUN ln -s /opt/toughadmin/etc/toughadmin /usr/bin/toughadmin && chmod +x /usr/bin/toughadmin
RUN rm -f /etc/nginx/nginx.conf && ln -s /opt/toughadmin/etc/nginx.conf /etc/nginx/nginx.conf
RUN ln -s /opt/toughadmin/etc/toughadmin-nginx.conf /etc/nginx/conf.d/toughadmin-nginx.conf

EXPOSE 1810

ENTRYPOINT ["/usr/bin/toughadmin","start"]

