#!/usr/bin/env python
# coding=utf-8

from twisted.internet import defer
from toughac.portal import cmcc, huawei
from toughac.acagent import base_handler

class AuthHandler(base_handler.BasicHandler):

    @defer.inlineCallbacks
    def proc_cmccv1(self, req):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_AUTH,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=self.config.ac.key
        )
        resp.attrNum = 1
        resp.attrs = [
            (0x05, 'success'),
        ]
        yield
        defer.returnValue(resp)

    @defer.inlineCallbacks
    def proc_cmccv2(self, req):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_AUTH,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=self.config.ac.key
        )
        resp.attrNum = 1
        resp.attrs = [
            (0x05, 'success'),
        ]
        yield
        defer.returnValue(resp)

    @defer.inlineCallbacks
    def proc_huaweiv1(self, req):
        resp = huawei.Portal.newMessage(
            huawei.ACK_AUTH,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=self.config.ac.key
        )
        resp.attrNum = 1
        resp.attrs = [
            (0x05, 'success'),
        ]
        yield
        defer.returnValue(resp)

    @defer.inlineCallbacks
    def proc_huawev2(self, req):
        resp = huawei.PortalV2.newMessage(
            huawei.ACK_AUTH,
            req.userIp,
            req.serialNo,
            req.reqId,
            auth=req.auth,
            secret=self.config.ac.key
        )
        resp.attrNum = 1
        resp.attrs = [
            (0x05, 'success'),
        ]
        resp.auth_packet()
        yield
        defer.returnValue(resp)

