#!/usr/bin/env python
# coding=utf-8
import sys, json
from twisted.python import log
from twisted.internet import reactor
from cyclone import httpclient
from hashlib import md5
from toughportal.common import logger

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
            self.syslog.error("ping admin server error,http status = %s" % resp.code)
            return

        jsonresp = json.loads(resp.body)
        if jsonresp['code'] == 0:
            if self.config.defaults.debug:
                self.syslog.debug("ping admin success")

        elif jsonresp['code'] == 1:
            self.syslog.error("ping admin server error, %s" % jsonresp['msg'])

        elif jsonresp['code'] == 100:
            self.syslog.info("portal didn't register, now join it")
            self.add_portal()

    def ping(self):
        sign = self.mksign(params=[self.config.portal.name, self.config.portal.ipaddr])
        reqdata = json.dumps(dict(name=self.config.portal.name, ip_addr=self.config.portal.ipaddr, sign=sign))

        if self.config.defaults.debug:
            self.syslog.debug("register portal request: %s" % reqdata)

        d = httpclient.fetch("%s/portal/ping" % self.config.api.apiurl,
                             postdata=reqdata, headers={"Content-Type": ["application/json"]})
        d.addCallback(self.on_ping)

    def on_add_portal(self, resp):
        if self.config.defaults.debug:
            log.msg(resp.body)

        if resp.code != 200:
            self.syslog.error("register portal to admin server error,http status = %s" % resp.code)
            return

        jsonresp = json.loads(resp.body)

        if jsonresp['code'] == 0:
            self.syslog.info("register portal success")

        elif jsonresp['code'] == 1:
            self.syslog.error("register portal server error, %s" % jsonresp['msg'])

    def add_portal(self):
        sign = self.mksign(params=[
            self.config.portal.name,
            self.config.portal.ipaddr,
            self.config.portal.secret,
            self.config.portal.port,
            self.config.portal.listen
        ])
        reqdata = json.dumps(dict(
            name=self.config.portal.name,
            ip_addr=self.config.portal.ipaddr,
            secret=self.config.portal.secret,
            http_port=self.config.portal.port,
            listen_port=self.config.portal.listen,
            sign=sign
        ))
        if self.config.defaults.debug:
            self.syslog.debug("register portal request:  %s" % reqdata)
        d = httpclient.fetch("%s/portal/add" % self.config.api.apiurl,
                             postdata=reqdata, headers={"Content-Type": ["application/json"]})

        d.addCallback(self.on_add_portal)

    def process(self):
        try:
            self.ping()
        except Exception as err:
            log.err(err, 'ping process error')

        reactor.callLater(120, self.process, )


def run(config):
    log.startLogging(sys.stdout)
    log.msg("start ping task")
    app = PingProc(config)
    app.process()


