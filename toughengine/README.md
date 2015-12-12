# ToughEngine 

ToughEngine is an AAA engine stripped out from [ToughRADIUS](https://github.com/talkincode/ToughRADIUS "ToughRADIUS") project  to achieve the standard Radius protocol, and support for Radius protocol extensions, ToughEngine via API interfaces to integrate back-end user management system, ToughEngine can be understood as a Radius middleware.

## system architecture

![image](https://cloud.githubusercontent.com/assets/377938/10863076/cb321bec-7ffc-11e5-9153-1971745efe4d.png)


## quickstart

    $ mkdir -p /home/var/toughengine
    
    $ vi /etc/toughengine.env
    
    NAS_FETCH_URL=http://127.0.0.1:1815/test/nas/all
    NAS_FETCH_SECRET=rpWE9AtfDPQ3ufXBS6gJ37WW8TnSF930
    SYSLOG_ENABLE=0
    SYSLOG_SERVER=127.0.0.1
    SYSLOG_PORT=514
    SYSLOG_LEVEL=INFO
    TIMEZONE=CST-8

    $ docker run  -d  --name tengine -v /home/var/toughengine:/var/toughengine  \
        --env-file=/etc/toughengine.env \
        -p 1812:1812/udp -p 1813:1813/udp  -p 1815:1815  \
        talkincode/toughengine