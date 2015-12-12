#!/usr/bin/env python
# coding=utf-8

from twisted.python import log
from twisted.internet import protocol
from twisted.internet import reactor
from toughac.portal import cmcc,pktutils
from toughac.common import logger


class HuaweiAgent(protocol.DatagramProtocol):
    def __init__(self, config):
        self.config = config
        self.syslog = logger.Logger(self.config)


    def doAckChellenge(self, req):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_CHALLENGE,
            req.userIp,
            req.serialNo,
            cmcc.CurrentSN(),
            secret=self.config.ac.key
        )
        resp.attrNum = 2
        resp.attrs = [
            (0x03, '\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'),
            (0x0a, '\x7f\x00\x00\x01')
        ]
        return resp

    def doAckAuth(self, req):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_AUTH,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=self.config.ac.key
        )
        resp.attrNum = 2
        resp.attrs = [
            (0x0a, '\x7f\x00\x00\x01'),
            (0x0b, '\x01\x02\x03\x04\x05\x06')
        ]
        return resp

    def doAckLogout(self, req):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_LOGOUT, req.userIp,
            req.serialNo, 0,
            secret=self.config.ac.key
        )
        resp.attrNum = 1
        resp.attrs = [
            (0x0a, '\x7f\x00\x00\x01')
        ]
        resp.auth_packet()

        resp2 = cmcc.Portal.newMessage(
            cmcc.NTF_LOGOUT, req.userIp,
            0, req.reqId,
            secret=self.config.ac.key
        )
        reactor.callLater(1, self.sendtoPortald, resp2)
        return resp

    def doAckInfo(self, req):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_INFO,
            req.userIp,
            req.serialNo,
            0,
            auth=req.auth,
            secret=self.config.ac.key
        )
        resp.attrNum = 1
        resp.attrs = [
            (0x0a, '\x7f\x00\x00\x01')
        ]
        return resp

    def sendtoPortald(self, msg):
        portal_addr = (
            self.config.portal.host,
            int(self.config.portal.listen)
        )
        self.syslog.debug(":: Send Message to Portal Listen %s: %s" % (portal_addr, repr(msg)))
        self.transport.write(str(msg), portal_addr)

    def datagramReceived(self, datagram, (host, port)):
        try:
            print
            log.msg("*" * 120)
            print

            print pktutils.hexdump(datagram, len(datagram))
            _packet = cmcc.Portal(secret=self.config.ac.key, packet=datagram, source=(host, port))
            self.syslog.debug(":: Received portal packet from %s:%s: %s" % (host, port, repr(_packet)))
            resp = None
            if _packet.type == cmcc.REQ_CHALLENGE:
                resp = self.doAckChellenge(_packet)
            elif _packet.type == cmcc.REQ_AUTH:
                resp = self.doAckAuth(_packet)
            elif _packet.type == cmcc.REQ_LOGOUT:
                resp = self.doAckLogout(_packet)
            elif _packet.type == cmcc.REQ_INFO:
                resp = self.doAckInfo(_packet)
            elif _packet.type == cmcc.AFF_ACK_AUTH:
                pass
            elif _packet.type == cmcc.ACK_NTF_LOGOUT:
                pass
            elif _packet.type == cmcc.NTF_HEARTBEAT:
                pass
            else:
                log.msg("not support packet type: %s" % _packet.type)
            print
            if resp:
                print pktutils.hexdump(str(resp), len(resp))
                self.syslog.debug(":: Send response to %s:%s: %s" % (host, port, repr(resp)))
                self.transport.write(str(resp), (host, port))
        except Exception as err:
            self.syslog.error(':: Dropping invalid packet from %s: %s' % ((host, port), str(err)))
            import traceback
            traceback.print_exc()

    def on_exception(self, err):
        self.syslog.error(':: Packet process error：%s' % str(err))

    def run_normal(self):
        self.syslog.info('running cmcc acagent server')
        reactor.listenUDP(int(self.config.ac.port), self)
        reactor.run()


def run(config):
    portal = HuaweiAgent(config)
    portal.run_normal()