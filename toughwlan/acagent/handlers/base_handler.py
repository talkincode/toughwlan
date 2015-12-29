#!/usr/bin/env python
# coding=utf-8

from twisted.internet import defer
from txradius import client
import functools

class ACError(BaseException):
    pass


class BasicHandler:
    def __init__(self, config, syslog, radius_dict=None):
        self.config = config
        self.syslog = syslog
        self.radius_dict = radius_dict

    @defer.inlineCallbacks
    def process(self, req):
        if 'cmccv1' in self.config.ac.vendor:
            resp = yield self.proc_cmccv1(req)
            defer.returnValue(resp)
        elif 'cmccv2' in self.config.ac.vendor:
            resp = yield self.proc_cmccv2(req)
            defer.returnValue(resp)
        elif 'huaweiv1' in self.config.ac.vendor:
            resp = yield self.proc_huaweiv1(req)
            defer.returnValue(resp)
        elif 'huaweiv2' in self.config.ac.vendor:
            resp = yield self.proc_huaweiv2(req)
            defer.returnValue(resp)
        else:
            raise ACError("vendor {0} not support".format(self.config.ac.vendor))

    @defer.inlineCallbacks
    def proc_cmccv1(self, req):
        raise ACError("does not support")

    @defer.inlineCallbacks
    def proc_cmccv2(self, req):
        raise ACError("does not support")

    @defer.inlineCallbacks
    def proc_huaweiv1(self, req):
        raise ACError("does not support")

    @defer.inlineCallbacks
    def proc_huaweiv2(self, req):
        raise ACError("does not support")


class EmptyHandler(BasicHandler):
    @defer.inlineCallbacks
    def process(self, req):
        yield
        self.syslog.debug("do nothing for {0}".format(repr(req)))
        defer.returnValue(None)