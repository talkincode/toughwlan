#!/usr/bin/env python
# coding=utf-8

from twisted.internet import defer
from txportal.packet import cmcc, huawei
from toughwlan.acagent.handlers import base_handler
from toughwlan.acagent.session import RadiusSession
from txradius.radius.tools import DecodeAddress

class AuthHandler(base_handler.BasicHandler):

    def proc_cmccv1(self, req):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_AUTH,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=str(self.config.acagent.secret)
        )
        resp.attrNum = 1
        resp.attrs = [
            (0x05, 'success'),
        ]

        return  defer.succeed(resp)

    def proc_cmccv2(self, req):
        resp = cmcc.Portal.newMessage(
            cmcc.ACK_AUTH,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=str(self.config.acagent.secret)
        )
        resp.attrNum = 1
        resp.attrs = [
            (0x05, 'success'),
        ]
        return  defer.succeed(resp)

    def proc_huaweiv1(self, req):
        resp = huawei.Portal.newMessage(
            huawei.ACK_AUTH,
            req.userIp,
            req.serialNo,
            req.reqId,
            secret=str(self.config.acagent.secret)
        )
        resp.attrNum = 1
        resp.attrs = [
            (0x05, 'success'),
        ]
        return  defer.succeed(resp)

    @defer.inlineCallbacks
    def proc_huaweiv2(self, req):
        username = req.get_user_name()
        password = req.get_password()
        challenge = req.get_challenge()
        chap_pwd = req.get_chap_pwd()
        userip = DecodeAddress(req.userIp)

        # import pdb;pdb.set_trace()
        session = RadiusSession(self.config, self.radius_loader.getMasterRadius(),self.syslog)
        rad_resp = yield session.start(username,password,challenge,chap_pwd,userip=userip)
        if rad_resp and rad_resp['code'] == 0:
            resp = huawei.PortalV2.newMessage(
                huawei.ACK_AUTH,
                req.userIp,
                req.serialNo,
                req.reqId,
                str(self.config.acagent.secret)
                auth=req.auth,
                chap=(req.isChap==0x00)
            )
            resp.attrNum = 1
            resp.attrs = [
                (0x05, 'success'),
            ]
            resp.auth_packet()
            defer.returnValue(resp)
        else:
            resp = huawei.PortalV2.newMessage(
                huawei.ACK_AUTH,
                req.userIp,
                req.serialNo,
                req.reqId,
                str(self.config.acagent.secret)
                auth=req.auth,
                chap=(req.isChap==0x00)
            )
            resp.errCode=4
            resp.attrNum = 1
            resp.attrs = [
                (0x05, (rad_resp or {}).get('msg','no radius resp')),
            ]
            resp.auth_packet()
            defer.returnValue(resp)


