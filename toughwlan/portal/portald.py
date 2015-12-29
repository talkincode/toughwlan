#!/usr/bin/env python
#coding=utf-8
import sys
import time
import os
from twisted.python import log
from twisted.internet import task
from twisted.internet import protocol
from twisted.internet import reactor
from txportal.packet import cmcc, huawei
from toughlib import utils, logger

class Vendor:
    def __init__(self, name, mod, proto):
        self.name = name
        self.mod = mod
        self.proto = proto

class PortalListen(protocol.DatagramProtocol):

    vendors = {
        'cmccv1': Vendor('cmccv1', cmcc, cmcc.Portal),
        'cmccv2': Vendor('cmccv2', cmcc, cmcc.Portal),
        'huaweiv1': Vendor('huaweiv1', huawei, huawei.Portal),
        'huaweiv2': Vendor('huaweiv2', huawei, huawei.PortalV2),
    }
    
    actions = {}
    
    def __init__(self, config, log=None):
        self.syslog = log or logger.Logger(config)
        self.config = config
        self.vendor = PortalListen.vendors.get(config.portal.vendor)
        self.actions = {
            self.vendor.mod.NTF_LOGOUT : self.doAckNtfLogout
        }
        reactor.callLater(3.0,self.init_task)
        
        
    def init_task(self):
        _task = task.LoopingCall(self.send_ntf_heart)
        _task.start(self.config.portal.ntf_heart)
    
    def send_ntf_heart(self):
        pass
        # host,port = self.ac1[0], int(self.ac1[1])
        # req = self.vendor.Portal.newNtfHeart(self.config.portal.secret,host)
        # if self.debug:
        #     pass
        #     # self.syslog.info("Send NTF_HEARTBEAT to %s:%s: %s" % (host,port,repr(req)))
        # try:
        #     self.transport.write(str(req), (host,port))
        # except:
        #     pass
            
    def doAckNtfLogout(self,req,(host, port)):
        resp = self.vendor.proto.newMessage(
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
        try:
            req = self.vendor.proto(
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

        
def run(config, log=None):
    app = PortalListen(config, log=log)
    reactor.listenUDP(int(config.portal.listen), app,interface=config.portal.host)


