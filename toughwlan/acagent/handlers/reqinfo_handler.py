#!/usr/bin/env python
# coding=utf-8

from twisted.internet import defer
from txportal.packet import cmcc, huawei
from toughwlan.acagent.handlers import base_handler

class AuthHandler(base_handler.BasicHandler):

    def proc_cmccv1(self, req, rundata):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_INFO,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=str(self.config.acagent.secret)
        )
        return  defer.succeed(resp)

    
    def proc_cmccv2(self, req, rundata):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_INFO,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=str(self.config.acagent.secret)
        )
        return  defer.succeed(resp)

    def proc_huaweiv1(self, req, rundata):
        resp = huawei.Portal.newMessage(
            huawei.ACK_INFO,
            req.userIp,
            req.serialNo,
            req.reqId,
            str(self.config.acagent.secret)
        )
        return  defer.succeed(resp, rundata)

    def proc_huawev2(self, req, rundata):
        resp = huawei.Portal.newMessageV2(
            huawei.ACK_INFO,
            req.userIp,
            req.serialNo,
            req.reqId,
            str(self.config.acagent.secret),
            auth=req.auth,
        )
        resp.auth_packet()
        return  defer.succeed(resp, rundata)

