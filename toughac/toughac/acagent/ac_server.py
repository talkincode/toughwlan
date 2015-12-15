#!/usr/bin/env python
# coding=utf-8

from twisted.internet import protocol
from twisted.internet import reactor
from toughac.portal import cmcc, huawei, pktutils
from toughac.common import logger
from toughac.acagent import auth_handler, chellenge_handler, base_handler

ACError = base_handler.ACError



class AcServer(protocol.DatagramProtocol):
    def __init__(self, config):
        self.config = config
        self.syslog = logger.Logger(self.config)
        self.ac_handlers = {
            cmcc.REQ_CHALLENGE : chellenge_handler.ChellengeHandler(self.config, self.syslog),
            cmcc.REQ_AUTH      : auth_handler.AuthHandler(self.config, self.syslog),
            cmcc.REQ_INFO      : auth_handler.AuthHandler(self.config, self.syslog),
            cmcc.AFF_ACK_AUTH  : base_handler.EmptyHandler(self.config, self.syslog),
            cmcc.ACK_NTF_LOGOUT: base_handler.EmptyHandler(self.config, self.syslog),
            cmcc.NTF_HEARTBEAT : base_handler.EmptyHandler(self.config, self.syslog),
        }

    def sendtoPortald(self, msg):
        portal_addr = (
            self.config.portal.host,
            int(self.config.portal.listen)
        )
        self.syslog.debug(":: Send Message to Portal Listen %s: %s" % (portal_addr, repr(msg)))
        self.transport.write(str(msg), portal_addr)

    def parse(self, datagram, (host, port)):
        # import pdb
        # pdb.set_trace()
        if self.config.ac.vendor in ('cmccv1', 'cmccv2'):
            return cmcc.Portal(secret=self.config.ac.key, packet=datagram, source=(host, port))
        elif 'huaweiv1' in self.config.ac.vendor:
            return huawei.Portal(ver=0x01, secret=self.config.ac.key, packet=datagram, source=(host, port))
        elif 'huaweiv2' in self.config.ac.vendor:
            return huawei.Portal(ver=0x02, secret=self.config.ac.key, packet=datagram, source=(host, port))
        else:
            raise ACError("vendor {0} not support".format(self.config.ac.vendor))

    def datagramReceived(self, datagram, (host, port)):
        def send_resp(resp):
            if resp:
                self.transport.write(str(resp), (host, port))
                print pktutils.hexdump(str(resp), len(resp))
                self.syslog.debug(":: Send response to %s:%s: %s" % (host, port, repr(resp)))

        try:
            print pktutils.hexdump(datagram, len(datagram))
            request = self.parse(datagram, (host, port))
            self.syslog.debug(":: Received portal packet from %s:%s: %s" % (host, port, repr(request)))
            resp_deferd = self.ac_handlers[request.type].process(request)
            resp_deferd.addCallback(send_resp)
        except Exception as err:
            self.syslog.error(':: Dropping invalid packet from %s: %s' % ((host, port), str(err)))
            import traceback
            traceback.print_exc()

    def on_exception(self, err):
        self.syslog.error(':: Packet process error：%s' % str(err))

    def run_normal(self):
        self.syslog.info('running ac server')
        reactor.listenUDP(int(self.config.ac.port), self)
        reactor.run()


def run(config):
    portal = AcServer(config)
    portal.run_normal()