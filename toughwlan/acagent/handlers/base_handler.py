#!/usr/bin/env python
# coding=utf-8

from twisted.internet import defer
from txradius import client
import functools

class ACError(BaseException):
    pass


class BasicHandler:
    def __init__(self, config, syslog, radius_dict=None,radius_loader=None):
        self.config = config
        self.syslog = syslog
        self.radius_dict = radius_dict
        self.radius_loader = radius_loader

    def process(self, req):
        if 'cmccv1' in self.config.acagent.vendor:
            return self.proc_cmccv1(req)
        elif 'cmccv2' in self.config.acagent.vendor:
            return self.proc_cmccv2(req)
        elif 'huaweiv1' in self.config.acagent.vendor:
            return self.proc_huaweiv1(req)
        elif 'huaweiv2' in self.config.acagent.vendor:
            return self.proc_huaweiv2(req)
        else:
            raise ACError("vendor {0} not support".format(self.config.acagent.vendor))


    def proc_cmccv1(self, req):
        raise ACError("does not support")

    def proc_cmccv2(self, req):
        raise ACError("does not support")

    def proc_huaweiv1(self, req):
        raise ACError("does not support")

    def proc_huaweiv2(self, req):
        raise ACError("does not support")


class EmptyHandler(BasicHandler):

    def process(self, req):
        self.syslog.debug("do nothing for {0}".format(repr(req)))
        return None