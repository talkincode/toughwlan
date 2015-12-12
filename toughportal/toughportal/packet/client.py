#!/usr/bin/env python
#coding=utf-8
from twisted.internet import defer
from twisted.internet import protocol
from twisted.internet import reactor
from toughportal.packet import cmcc, huawei
from toughportal.common import utils, logger,config
from toughportal.packet.pktutils import hexdump
import time
import six

vendors = {
    'cmcc': cmcc,
    'huawei': huawei
}

class Timeout(Exception):
    """Simple exception class which is raised when a timeout occurs
    while waiting for a ac server to respond."""


def sleep(secs):
    d = defer.Deferred()
    reactor.callLater(secs, d.callback, None)
    return d

class PortalClient(protocol.DatagramProtocol):
    
    results = {}
    
    def __init__(self,secret=six.b(''), timeout=10, retry=3, debug=True, syslog=None, vendor='cmcc'):
        self.secret = secret
        self.timeout = timeout
        self.retry = retry
        self.debug = debug
        self.syslog = syslog or logger.Logger(config.find_config())
        self.vendor = vendors.get(vendor)
        self.port = reactor.listenUDP(0, self)
        
    def close(self):
        self.transport = None
        self.results.clear()
        self.port.stopListening()

    @defer.inlineCallbacks
    def sendto(self,req,(host,port),recv=True):
        if self.debug:
            print ":: Hexdump >> %s" % hexdump(str(req),len(req))

        self.syslog.info("Start send packet To AC (%s:%s) >> %s"%(host,port,repr(req)))
        
        if not recv:
            self.transport.write(str(req),(host,port))
            return

        for attempt in range(self.retry):
            self.syslog.info("Send portal packet times %s" % attempt)
            self.transport.write(str(req),(host,port))
            now = time.time()
            waitto = now + self.timeout
            while now < waitto:
                if req.sid in self.results:
                    defer.returnValue(self.results.pop(req.sid))
                    return
                else:
                    now = time.time()
                    yield sleep(0.002)
                    continue

        raise Timeout("send packet timeout")


    def datagramReceived(self, datagram, (host, port)):
        try:
            if self.debug:
                print ":: Hexdump > %s"%hexdump(datagram,len(datagram))


            resp = self.vendor.Portal(packet=datagram,secret=self.secret)
            self.results[resp.sid] = resp
            self.syslog.info(":: Received <%s> packet from AC %s >> %s " % (self.vendor, (host, port), repr(resp)))

        except Exception as err:
            self.syslog.error('Process <%s> packet error  %s >> %s' % (self.vendor, (host, port), utils.safestr(err)))
