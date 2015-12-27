#!/usr/bin/env python
# coding=utf-8
import sys, struct
from twisted.internet import reactor
from twisted.internet import defer
from toughlib.dbengine import get_engine
from toughlib import logger, utils
from sqlalchemy.orm import scoped_session, sessionmaker
from toughwlan.console import models
from twisted.names import client, dns

class DDNSProc:

    def __init__(self, config, log=None):
        self.config = config
        self.log = log or logger.Logger(config)
        self.db = scoped_session(sessionmaker(bind=get_engine(config), autocommit=False, autoflush=True))

    @defer.inlineCallbacks
    def process(self):
        conn = self.db()
        try:
            nas = conn.query(models.TraBas)
            for line in lines:
                results, _, _ = yield client.lookupAddress(line.dns_name)
                if not results:
                    self.log.info("domain {0} resolver empty".format(line.dns_name))

                if results[0].type == dns.A:
                    ipaddr = ".".join(str(i) for i in struct.unpack("BBBB", results[0].payload.address))
                    if ipaddr:
                        line.ip_addr = ipaddr
                        conn.commit()
                        self.log.info("domain {0} resolver {1}  success".format(line.dns_name,ipaddr))
                else:
                    self.log.info("domain {0} no ip address,{1}".format(line.dns_name, repr(results)))

        except Exception as err:
            self.log.error('ddns process error %s' % utils.safeunicode(err.message))
        finally:
            conn.close()

        reactor.callLater(60, self.process, )

def run(config):
    app = DDNSProc(config)
    deferd = app.process()



