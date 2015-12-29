#!/usr/bin/env python
# coding=utf-8

from twisted.internet import defer
from txportal.packet import cmcc, huawei
from toughwlan.acagent.handlers import base_handler

class AuthHandler(base_handler.BasicHandler):

    @defer.inlineCallbacks
    def proc_cmccv1(self, req):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_INFO,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=self.config.ac.key
        )
        defer.returnValue(resp)

    @defer.inlineCallbacks
    def proc_cmccv2(self, req):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_INFO,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=self.config.ac.key
        )
        defer.returnValue(resp)

    @defer.inlineCallbacks
    def proc_huaweiv1(self, req):
        resp = huawei.Portal.newMessage(
            huawei.ACK_INFO,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=self.config.ac.key
        )
        defer.returnValue(resp)

    @defer.inlineCallbacks
    def proc_huawev2(self, req):
        resp = huawei.Portal.newMessageV2(
            huawei.ACK_INFO,
            req.userIp,
            req.serialNo,
            req.reqId,
            auth=req.auth,
            secret=self.config.ac.key
        )
        resp.auth_packet()
        defer.returnValue(resp)

