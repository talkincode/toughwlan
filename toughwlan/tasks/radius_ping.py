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

class RadiusPingProc(TaskProc):

    @defer.inlineCallbacks
    def ping(self):
        conn = self.db()
        try:
            for radius in conn.query(models.TraRadius):
                try:
                    reqdata = apiutils.make_message(radius.secret,action="ping")
                    resp = yield apiutils.request(portal.admin_url, data=reqdata)

                    jsonresp = json.loads(resp.body)
                    if jsonresp['code'] == 0:
                        radius.last_check = utils.get_currtime()

                except Exception as err:
                    defer.returnValue("ping radius <%s> error, %s" % (radius.ip_addr, str(err)))

            conn.commit()
            defer.returnValue("ping radius success")
        except Exception as err:
            defer.returnValue("ping radius error, %s" % str(err))
        finally:
            conn.close()


    def process(self):
        try:
            self.ping().addCallback(self.syslog.debug)
        except Exception as err:
            self.syslog.error('ping radius error, %s' % str(err))

        reactor.callLater(240, self.process, )


def run(config):
    log.msg("start radius ping task")
    app = RadiusPingProc(config)
    app.process()
    reactor.run()


