#!/usr/bin/env python
# coding=utf-8
import sys, json
import time
from twisted.python import log
from twisted.internet import reactor, defer
from cyclone import httpclient
from toughadmin.tasks.task_proc import TaskProc
from toughadmin.common import utils
from toughadmin.console import models

class RadiusPingProc(TaskProc):

    @defer.inlineCallbacks
    def ping(self):
        conn = self.db()
        try:
            nonce = str(time.time())
            action = "ping"
            headers = {"Content-Type": ["application/json"]}
            for radius in conn.query(models.TraRadius):
                try:
                    sign = self.mksign(radius.secret, params=[action, nonce])
                    reqdata = json.dumps(dict(action=action, nonce=nonce, sign=sign))
                    resp = yield httpclient.fetch(radius.admin_url, postdata=reqdata, headers=headers)
                    if resp.code != 200:
                        self.syslog.error("ping radius <%s> error,http status = %s" % (radius.ip_addr, resp.code))
                        continue

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
    log.startLogging(sys.stdout)
    log.msg("start radius ping task")
    app = RadiusPingProc(config)
    app.process()
    reactor.run()


