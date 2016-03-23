#!/bin/sh

if [ ! -f "/var/toughwlan/data" ];then
    mkdir -p /var/toughwlan/data
fi

if [ ! -f "/var/toughwlan/.install" ];then
    pypy /opt/toughwlan/toughctl --initdb
    echo "ok" > /var/toughwlan/.install
    echo "init database ok!"
fi