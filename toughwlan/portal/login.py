#!/usr/bin/env python
# coding:utf-8

import time
from toughlib import utils, logger,dispatch
from toughwlan.portal.base import BaseHandler
from twisted.internet import defer
from toughlib.permit import permit
from txportal import client
import functools

@permit.route(r"/portal/login")
class LoginHandler(BaseHandler):

    def get(self):
        qstr = self.request.query
        wlan_params = self.get_wlan_params(qstr)
        ssid = wlan_params.get("ssid", "default")
        ispcode = wlan_params.get("ispcode", "default")

        if self.settings.debug:
            logger.info( u"Open portal auth page, wlan params:{0}".format(utils.safeunicode(wlan_params)))

        tpl = self.get_template_attrs(ssid,ispcode)
        self.render(self.get_login_template(tpl['tpl_path']), msg=None, tpl=tpl, qstr=qstr, **wlan_params)


    @defer.inlineCallbacks
    def post(self):
        qstr = self.get_argument("qstr", "")
        wlan_params = self.get_wlan_params(qstr)
        ssid = wlan_params.get("ssid", "default")
        ispcode = wlan_params.get("ispcode", "default")

        if not wlan_params:
            self.render_error(msg=u"Missing parameter: ssid,wlanuserip,wlanacip")
            return

        start_time = time.time()
        nas = self.get_nas(wlan_params.get("wlanacip",'127.0.0.1'))
        if not nas:
            self.render_error(msg=u"AC server {0} didn't  register ".format(wlan_params.get("wlanacip")))
            return

        ac_addr = nas['ip_addr']
        ac_port = int(nas['ac_port'])
        secret = utils.safestr(nas['bas_secret'])
        _vendor= utils.safestr(nas['portal_vendor'])
        if _vendor not in ('cmccv1','cmccv2','huaweiv1','huaweiv2'):
            self.render_error(msg=u"AC server portal_vendor {0} not support ".format(_vendor))
            return

        send_portal = functools.partial(
            client.send,
            secret,
            log=self.syslog,
            debug=self.settings.debug,
            vendor=_vendor
        )
        vendor = client.PortalClient.vendors.get(_vendor)

        is_chap=self.settings.config.portal.chap in (1, "1", "chap")
        userIp=wlan_params.get('wlanuserip', self.request.remote_ip)
        username=self.get_argument("username", None)
        password=self.get_argument("password", None)

        if self.settings.debug:
            logger.info( u"Start [username:%s] portal auth, wlan params:%s" % (
                username, utils.safeunicode(wlan_params)))

        tpl = self.get_template_attrs(wlan_params.get("ssid", "default"))
        firsturl=tpl.get("home_page", "/portal/index?tpl_name=%s" % tpl.get('tpl_name', 'default'))

        def back_login(msg = u''):
            self.render(self.get_login_template(tpl['tpl_path']), tpl = tpl, msg = msg, qstr = qstr, **wlan_params)

        if not username or not password:
            back_login(msg = u"username and password cannot be empty")
            return

        # checkos
        # cli_dev, cli_os = self.chk_os
        # domain = yield self.get_domain(wlan_params.get("ssid", "default"))
        # username = "%s#%s#%s@%s" % (username, cli_dev, cli_os, domain)

        try:
            challenge_resp = None
            if is_chap:
                ## req challenge ################################
                challenge_req=vendor.proto.newReqChallenge(userIp, secret, chap = is_chap)
                challenge_resp = yield send_portal(data = challenge_req, host=ac_addr, port=ac_port)

                if challenge_resp.errCode > 0:
                    if challenge_resp.errCode == 2:
                        self.set_session_user(username, userIp, utils.get_currtime(), qstr=qstr)
                        self.redirect(firsturl)
                        return
                    raise Exception(vendor.mod.AckChallengeErrs[challenge_resp.errCode])

            if challenge_resp:
                ## req auth ################################
                auth_req = vendor.proto.newReqAuth(
                    userIp, username, password, challenge_resp.reqId, challenge_resp.get_challenge(), 
                    secret, ac_addr, serialNo=challenge_req.serialNo, chap=is_chap)
            else:
                auth_req = vendor.proto.newReqAuth(userIp, username,password,0,None,secret,ac_addr,chap=is_chap)

            auth_resp = yield send_portal(data=auth_req, host=ac_addr, port=ac_port)

            if auth_resp.errCode > 0:
                if auth_resp.errCode == 2:
                    self.set_session_user(username, userIp, utils.get_currtime(),qstr=qstr)
                    self.redirect(firsturl)
                    return
                _err_msg=u"{0},{1}".format(
                    vendor.mod.AckAuthErrs[auth_resp.errCode], 
                    utils.safeunicode(auth_resp.get_text_info()[0] or "")
                )
                raise Exception(_err_msg)

            ### aff_ack ################################
            affack_req = vendor.proto.newAffAckAuth(
                userIp, secret,ac_addr,auth_req.serialNo,auth_resp.reqId, chap = is_chap)

            send_portal(data=affack_req, host=ac_addr, port=ac_port)

            logger.info( u'Portal [username:{0}] auth success'.format(username))

            if self.settings.debug:
                logger.debug( u'Portal [username:%s] auth login [cast:%s ms]' % (
                username, (time.time() - start_time) * 1000))

            self.set_session_user(username, userIp, utils.get_currtime(),qstr=qstr, nasaddr=ac_addr)
            self.redirect(firsturl)

        except Exception as err:
            import traceback
            traceback.print_exc()
            back_login(msg = u"Portal auth error,%s" % utils.safeunicode(err.message))


