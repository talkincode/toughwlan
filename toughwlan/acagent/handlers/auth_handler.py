#!/usr/bin/env python
# coding=utf-8

from twisted.internet import defer
from txportal.packet import cmcc, huawei
from toughwlan.acagent.handlers import base_handler
from toughwlan.acagent.session import RadiusSession


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

        username = req.get_user_name()
        password = get_password()
        challenge = req.get_challenge()
        chap_pwd = req.get_chap_pwd()
        userip = req.userIp

        session = RadiusSession(self.config, 
            self.config.radius.master_key, 
            self.radius_dict, 
            self.config.radius.master_server)

        rad_resp = yield session.auth(username,password,challenge,chap_pwd)
        if rad_resp and rad_resp['code'] == 0:
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
            defer.returnValue(resp)
        else:
            resp = huawei.PortalV2.newMessage(
                huawei.ACK_AUTH,
                req.userIp,
                req.serialNo,
                req.reqId,
                errCode=4,
                auth=req.auth,
                secret=self.config.ac.key
            )
            resp.attrNum = 1
            resp.attrs = [
                (0x05, (rad_resp or {}).get('msg','no radius resp')),
            ]
            resp.auth_packet()
            defer.returnValue(resp)


