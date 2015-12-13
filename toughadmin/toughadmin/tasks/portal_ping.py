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

class PortalPingProc(TaskProc):

    @defer.inlineCallbacks
    def ping(self):
        conn = self.db()
        try:
            nonce = str(time.time())
            action = "ping"
            headers = {"Content-Type": ["application/json"]}
            for portal in conn.query(models.TraPortal):
                try:
                    sign = self.mksign(portal.secret, params=[action, nonce])
                    reqdata = json.dumps(dict(action=action, nonce=nonce, sign=sign))
                    resp = yield httpclient.fetch(portal.admin_url, postdata=reqdata, headers=headers)
                    if resp.code != 200:
                        self.syslog.error("ping portal <%s> error,http status = %s" % (portal.ip_addr, resp.code))
                        continue

                    jsonresp = json.loads(resp.body)
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
    log.startLogging(sys.stdout)
    log.msg("start portal ping task")
    app = PortalPingProc(config)
    app.process()
    reactor.run()


