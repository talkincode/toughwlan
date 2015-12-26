#!/usr/bin/env python
# coding=utf-8
import sys, json
import time
from twisted.python import log
from twisted.internet import reactor, defer
from cyclone import httpclient
from toughwlan.tasks.task_proc import TaskProc
from toughlib import utils
from toughwlan.console import models

class PortalPingProc(TaskProc):

    @defer.inlineCallbacks
    def ping(self):
        conn = self.db()
        try:
            for portal in conn.query(models.TraPortal):
                try:
                    reqdata = apiutils.make_message(portal.secret,action="ping")
                    resp = yield apiutils.request(portal.admin_url, data=reqdata)
                    jsonresp = yield resp.json()
                    if jsonresp['code'] == 0:
                        portal.last_check = utils.get_currtime()

                except Exception as err:
                    defer.returnValue("ping portal <%s> error, %s" % (portal.ip_addr, str(err)))

            conn.commit()
            defer.returnValue("ping portals success")
        except Exception as err:
            defer.returnValue("ping portals error, %s" % str(err))
        finally:
            conn.close()


    def process(self):
        try:
            self.ping().addCallback(self.syslog.debug)
        except Exception as err:
            self.syslog.error('ping portal error, %s' % str(err))

        reactor.callLater(240, self.process, )


def run(config):
    log.msg("start portal ping task")
    app = PortalPingProc(config)
    app.process()
    reactor.run()


