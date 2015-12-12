#!/usr/bin/env python
#coding=utf-8
import sys
import time
import os

from twisted.python import log
from twisted.internet import task
from twisted.internet import protocol
from twisted.internet import reactor

from toughportal.packet import cmcc, huawei
from toughportal.common import utils, logger

vendors = {
    'cmcc'  : cmcc,
    'huawei': huawei
}

class PortalListen(protocol.DatagramProtocol):
    
    actions = {}
    
    def __init__(self, config):
        self.syslog = logger.Logger(config)
        self.config = config
        self.vendor = vendors.get(config.portal.vendor)
        self.init_config()
        self.actions = {
            self.vendor.NTF_LOGOUT : self.doAckNtfLogout
        }
        reactor.callLater(5,self.init_task)
        
    def init_config(self):
        try:
            os.environ["TZ"] = self.timezone
            time.tzset()
        except:pass
        
    def init_task(self):
        _task = task.LoopingCall(self.config.portal.send_ntf_heart)
        _task.start(self.config.portal.ntf_heart)
    
    def send_ntf_heart(self):
        host,port = self.ac1[0], int(self.ac1[1])
        req = self.vendor.Portal.newNtfHeart(self.config.portal.secret,host)
        if self.debug:
            pass
            # self.syslog.info("Send NTF_HEARTBEAT to %s:%s: %s" % (host,port,repr(req)))
        try:
            self.transport.write(str(req), (host,port))
        except:
            pass
        
    def validAc(self,host):
        if host in [self.ac1, '10.10.10.254']:
            return self.ac1
        if self.ac2 and host in self.ac2:
            return self.ac2
            
    def doAckNtfLogout(self,req,(host, port)):
        resp = self.vendor.Portal.newMessage(
            self.vendor.ACK_NTF_LOGOUT,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret =self.config.portal.secret
        )

        try:
            self.syslog.info("Send portal packet to %s:%s: %s"%(host,port, utils.safestr(req)))
            self.transport.write(str(resp), (host, port))
        except:
            pass
            
    
    def datagramReceived(self, datagram, (host, port)):
        ac = self.validAc(host)
        if not ac:
            return self.syslog.info('Dropping packet from unknown ac host ' + host)
        try:
            req = self.vendor.Portal(
                secret=self.secret,
                packet=datagram,
                source=(host, port)
            )
            self.syslog.info("Received portal packet from %s:%s: %s"%(host,port,utils.safestr(req)))
            if req.type in self.actions:
                self.actions[req.type](req,(host, port))
            else:
                self.syslog.error('Not support packet from ac host ' + host)
                
        except Exception as err:
            self.syslog.error('Dropping invalid packet from %s: %s' % ((host, port), utils.safestr(err)))
 
    def on_exception(self, err):
        self.syslog.error('Packet process error：%s' % utils.safestr(err))
        
    def run_normal(self):
        log.startLogging(sys.stdout)
        self.syslog.info('portal server listen %s' % self.config.portal.host)
        reactor.listenUDP(int(self.config.portal.listen), self,interface=self.config.portal.host)
        # reactor.run()
            

        
def run(config):
    print 'running portal server...'
    portal = PortalListen(config)
    portal.run_normal()


