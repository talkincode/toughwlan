#!/bin/sh

if [ ! -f "/var/toughwlan/data" ];then
    mkdir -p /var/toughwlan/data
fi

if [ ! -f "/var/toughwlan/.install" ];then
    pypy /opt/toughwlan/wlanctl initdb -c /etc/toughwlan.json
    echo "ok" > /var/toughwlan/.install
    echo "init database ok!"
fi

exec "$@"