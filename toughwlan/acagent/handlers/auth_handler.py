#!/usr/bin/env python
# coding=utf-8
import struct
from twisted.internet import defer
from txportal.packet import cmcc, huawei
from toughlib import httpclient as requests
from toughlib import utils, logger, dispatch
from toughwlan.acagent.handlers import base_handler
from toughwlan.acagent.session import RadiusSession
from txradius.radius.tools import DecodeAddress
import functools

class AuthHandler(base_handler.BasicHandler):

    def proc_cmccv1(self, req, rundata):
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

    def proc_cmccv2(self, req, rundata):
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

    def proc_huaweiv1(self, req, rundata):
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
    def proc_huaweiv2(self, req, rundata):
        username = req.get_user_name()
        password = req.get_password()
        challenge = rundata['challenges'].get(req.sid)
        chap_pwd = req.get_chap_pwd()
        if chap_pwd and len(chap_pwd) == 16:
            chap_pwd = '%s%s' % (struct.pack('>H', req.reqId)[1],chap_pwd)
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
                str(self.config.acagent.secret),
                auth=req.auth,
                chap=(req.isChap==0x00)
            )
            resp.attrNum = 1
            resp.attrs = [
                (0x05, 'success'),
            ]
            resp.auth_packet()
            self.callback(userip,code=0)
            defer.returnValue(resp)
        else:
            resp = huawei.PortalV2.newMessage(
                huawei.ACK_AUTH,
                req.userIp,
                req.serialNo,
                req.reqId,
                str(self.config.acagent.secret),
                auth=req.auth,
                chap=(req.isChap==0x00)
            )
            resp.errCode=4
            resp.attrNum = 1
            resp.attrs = [
                (0x05, (rad_resp or {}).get('msg','no radius resp')),
            ]
            resp.auth_packet()
            self.callback(userip,code=1)
            defer.returnValue(resp)


    def callback(self,userip,code=0):
        cache_key = "callback_cache_%s" % utils.safestr(userip)
        notify_url = self.mcache.get(cache_key)
        logger.info("callback %s" % notify_url)
        if notify_url:
            notify_url = utils.safestr(notify_url.format(code=code))
            requests.get(notify_url).addCallbacks(logger.info,logger.error)



