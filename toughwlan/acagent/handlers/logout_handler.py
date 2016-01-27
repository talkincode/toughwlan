#!/usr/bin/env python
# coding=utf-8

from twisted.internet import defer
from txportal.packet import cmcc, huawei, pktutils
from toughwlan.acagent.handlers import base_handler
from toughwlan.acagent.session import RadiusSession

class LogoutHandler(base_handler.BasicHandler):

    def proc_cmccv1(self, req, rundata):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_LOGOUT,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=str(self.config.acagent.secret)
        )
        return  defer.succeed(resp)

    
    def proc_cmccv2(self, req, rundata):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_LOGOUT,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=str(self.config.acagent.secret)
        )
        return  defer.succeed(resp)

    def proc_huaweiv1(self, req, rundata):
        resp = huawei.Portal.newMessage(
            huawei.ACK_LOGOUT,
            req.userIp,
            req.serialNo,
            req.reqId,
            str(self.config.acagent.secret)
        )
        return  defer.succeed(resp)

    def proc_huaweiv2(self, req, rundata):
        
        resp = huawei.PortalV2.newMessage(
            huawei.ACK_LOGOUT,
            req.userIp,
            req.serialNo,
            req.reqId,
            str(self.config.acagent.secret),
            auth=req.auth,
            chap=(req.isChap==0x00)
        )
        resp.auth_packet()
        RadiusSession.stop_session(pktutils.DecodeAddress(req.userIp))

        return  defer.succeed(resp)



