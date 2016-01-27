#!/usr/bin/env python
# coding:utf-8

import time
from toughlib import utils
from toughwlan.portal.base import BaseHandler
from twisted.internet import defer
from toughlib.permit import permit
from txportal import client
import functools

@permit.route(r"/portal/logout")
class LogoutHandler(BaseHandler):

    @defer.inlineCallbacks
    def disconnect(self):
        try:
            is_chap=self.settings.config.portal.chap in (1, "1", "chap")
            userIp = self.current_user.ipaddr

            nas = self.get_nas(self.current_user.nasaddr)
            ac_addr = nas['ip_addr']
            ac_port = int(nas['ac_port'])
            secret = utils.safestr(nas['bas_secret'])
            _vendor= utils.safestr(nas['portal_vendor'])
            if _vendor not in ('cmccv1','cmccv2','huaweiv1','huaweiv2'):
                defer.returnValue("not support vendor %s"%_vendor)

            send_portal = functools.partial(
                client.send,
                secret,
                log=self.syslog,
                debug=self.settings.debug,
                vendor=_vendor
            )
            vendor = client.PortalClient.vendors.get(_vendor)
            logout_req = vendor.proto.newReqLogout(userIp, secret,chap=is_chap)
            logout_resp = yield send_portal(data=logout_req, host=ac_addr, port=ac_port)

            if logout_resp.errCode > 0:
                _err_msg=u"{0},{1}".format(
                    vendor.mod.AckLogoutErrs[logout_resp.errCode], 
                    utils.safeunicode(logout_resp.get_text_info()[0] or "")
                )
                logger.error( _err_msg)

            defer.returnValue("disconnect done!")
        except Exception as err:
            defer.returnValue(err)

    def get(self):
        if not self.current_user:
            self.redirect("/portal/login?ssid=default")
            return
        self.disconnect().addCallbacks(
            functools.partial(dispatch.pub(logger.EVENT_INFO)),
            functools.partial(dispatch.pub(logger.EVENT_ERROR)))
        qstr = self.current_user.get("qstr","ssid=default")
        self.clear_session()
        self.redirect("/portal/login?%s"%qstr,permanent=False)

