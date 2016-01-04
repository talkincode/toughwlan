#!/usr/bin/env python
# coding=utf-8
import sys,os
from twisted.internet import protocol
from twisted.internet import reactor, defer
from txportal.packet import cmcc, huawei, pktutils
from toughlib import logger
from toughwlan.acagent.handlers import auth_handler, chellenge_handler, base_handler
from toughwlan.acagent import radius_loader
from txradius.radius import dictionary
import toughwlan

ACError = base_handler.ACError

class AcPortald(protocol.DatagramProtocol):
    def __init__(self, config, log=None):
        self.config = config
        self.log = log or logger.Logger(self.config)
        self.radius_dict = dictionary.Dictionary(
            os.path.join(os.path.dirname(toughwlan.__file__),"dictionarys/dictionary"))
        self.radloader = radius_loader.RadiusLoader(config)

        self.ac_handlers = {
            cmcc.REQ_CHALLENGE : chellenge_handler.ChellengeHandler(self.config, self.log),
            cmcc.REQ_AUTH      : auth_handler.AuthHandler(
                                            self.config, self.log, 
                                            radius_dict=self.radius_dict,radius_loader=self.radloader ),
            cmcc.REQ_INFO      : auth_handler.AuthHandler(self.config, self.log),
            cmcc.AFF_ACK_AUTH  : base_handler.EmptyHandler(self.config, self.log),
            cmcc.ACK_NTF_LOGOUT: base_handler.EmptyHandler(self.config, self.log),
            cmcc.NTF_HEARTBEAT : base_handler.EmptyHandler(self.config, self.log),
        }

    def sendtoPortald(self, msg):
        portal_addr = (self.config.portal.host, int(self.config.portal.listen))
        if self.config.system.debug:
            self.log.debug(":: Send Message to Portal Listen %s: %s" % (portal_addr, repr(msg)))
        self.transport.write(str(msg), portal_addr)

    def parse(self, datagram, (host, port)):
        if self.config.acagent.vendor in ('cmccv1', 'cmccv2'):
            return cmcc.Portal(secret=self.config.acagent.secret, packet=datagram, source=(host, port))
        elif 'huaweiv1' in self.config.acagent.vendor:
            return huawei.Portal(secret=self.config.acagent.secret, packet=datagram, source=(host, port))
        elif 'huaweiv2' in self.config.acagent.vendor:
            return huawei.PortalV2(secret=self.config.acagent.secret, packet=datagram, source=(host, port))
        else:
            raise ACError("vendor {0} not support".format(self.config.acagent.vendor))

    @defer.inlineCallbacks
    def datagramReceived(self, datagram, (host, port)):
        try:
            request = self.parse(datagram, (host, port))
            if self.config.system.debug:
                self.log.debug(":: Received portal packet from %s:%s: %s" % (host, port, repr(request)))
            # import pdb;pdb.set_trace()
            handler = self.ac_handlers[request.type]
            resp = yield handler.process(request)

            if resp:
                self.transport.write(str(resp), (host, port))
                if self.config.system.debug:
                    self.log.debug(":: Send response to %s:%s: %s" % (host, port, repr(resp)))

        except Exception as err:
            self.log.error(':: Dropping invalid packet from %s: %s' % ((host, port), str(err)))
            import traceback
            traceback.print_exc()


def run(config, log=None):
    portald = AcPortald(config,log=log)
    reactor.listenUDP(int(config.acagent.port), portald)



