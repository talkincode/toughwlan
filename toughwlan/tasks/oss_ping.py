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
from toughlib import apiutils

class OssPingProc(TaskProc):

    @defer.inlineCallbacks
    def ping(self):
        conn = self.db()
        try:
            for oss in conn.query(models.TraOssServer):
                try:
                    reqdata = apiutils.make_message(oss.secret,action="ping")
                    resp = yield apiutils.request(oss.admin_url, data=reqdata)
                    jsonresp = yield resp.json()
                    if jsonresp['code'] == 0:
                        oss.last_check = utils.get_currtime()
                except Exception as err:
                    defer.returnValue("ping oss <%s> error, %s" % (oss.admin_url, str(err)))

            conn.commit()
            defer.returnValue("ping oss success")
        except Exception as err:
            defer.returnValue("ping oss error, %s" % str(err))
        finally:
            conn.close()


    def process(self):
        try:
            self.ping().addCallback(self.syslog.debug)
        except Exception as err:
            self.syslog.error('ping oss error, %s' % str(err))

        reactor.callLater(240, self.process, )


def run(config):
    log.msg("start oss ping task")
    app = OssPingProc(config)
    app.process()
    reactor.run()


