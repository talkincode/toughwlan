#!/usr/bin/env python
# coding=utf-8
import sys, json
from twisted.python import log
from twisted.internet import reactor
from cyclone import httpclient
from hashlib import md5
from toughengine.common import logger

class PingProc:
    def __init__(self, config):
        self.config = config
        self.syslog = logger.Logger(config)


    def mksign(self, params=[]):
        _params = [str(p) for p in params if p is not None]
        _params.sort()
        _params.insert(0, self.config.api.apikey)
        strs = ''.join(_params)
        return md5(strs.encode()).hexdigest().upper()

    def on_ping(self, resp):
        if self.config.defaults.debug:
            log.msg(resp.body)

        if resp.code != 200:
            self.syslog.error("radius ping admin server error,http status = %s" % resp.code)
            return

        jsonresp = json.loads(resp.body)
        if jsonresp['code'] == 0:
            if self.config.defaults.debug:
                self.syslog.debug("radius ping admin success")

        elif jsonresp['code'] == 1:
            self.syslog.error("radius ping admin server error, %s" % jsonresp['msg'])

        elif jsonresp['code'] == 100:
            self.syslog.info("radius didn't register")

    def ping(self):
        sign = self.mksign(params=[self.config.radiusd.name, self.config.radiusd.ipaddr])
        reqdata = json.dumps(dict(name=self.config.radiusd.name, ipaddr=self.config.radiusd.ipaddr, sign=sign))

        if self.config.defaults.debug:
            self.syslog.debug("radius ping admin request: %s" % reqdata)

        headers = {"Content-Type": ["application/json"]}
        d = httpclient.fetch("%s/radius/ping" % self.config.api.apiurl, postdata=reqdata, headers=headers)
        d.addCallback(self.on_ping)


    def process(self):
        try:
            self.ping()
        except Exception as err:
            self.syslog.error('ping process error, %s' % str(err))

        reactor.callLater(120, self.process, )


def run(config):
    log.startLogging(sys.stdout)
    log.msg("start ping task")
    app = PingProc(config)
    app.process()


