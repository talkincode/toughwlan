#!/usr/bin/env python
# coding=utf-8

from twisted.internet import defer
from txportal.packet import cmcc, huawei, pktutils
from toughwlan.acagent.handlers import base_handler

class ChellengeHandler(base_handler.BasicHandler):

    def proc_cmccv2(self, req, rundata):
        resp = huawei.Portal.newMessage(
            cmcc.ACK_CHALLENGE,
            req.userIp,
            req.serialNo,
            cmcc.CurrentSN(),
            secret=str(self.config.acagent.secret)
        )
        resp.attrNum = 1
        challenge = pktutils.CreateChallenge()
        resp.attrs = [
            (0x03, challenge)
        ]
        resp.auth_packet()
        rundata['challenges'][resp.sid] = challenge
        return  defer.succeed(resp)

    def proc_huaweiv2(self,req, rundata):
        resp = huawei.PortalV2.newMessage(
            huawei.ACK_CHALLENGE,
            req.userIp,
            req.serialNo,
            huawei.CurrentSN(),
            str(self.config.acagent.secret),
            auth=req.auth,
            chap=(req.isChap==0x00)
        )
        resp.attrNum = 1
        challenge = pktutils.CreateChallenge()
        resp.attrs = [
            (0x03, challenge)
        ]
        resp.auth_packet()
        rundata['challenges'][resp.sid] = challenge
        return  defer.succeed(resp)




