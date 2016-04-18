#!/usr/bin/env python
# coding:utf-8

import tornado.web
from twisted.internet import reactor, defer
from urllib import urlencode
from toughlib import logger,utils,dispatch
from toughlib.permit import permit
from toughlib import db_cache as cache
from toughlib.dbengine import get_engine
from toughwlan.manage.portal.base import BaseHandler

@permit.route(r"/portal/forward")
class ForwardHandler(BaseHandler):

    def get(self, *args, **kwargs):
        logger.info(utils.safeunicode(self.request.query))
        wlan_params = {
            "wlanuserip": self.get_argument("userip", self.request.remote_ip),
            "ispcode": self.get_argument("ispcode", "default"),
            "wlanusername": self.get_argument("username","test"),
            "wlanacip": self.settings['config'].acagent.nasaddr,
            "ssid": self.get_argument("ssid","default"),
            "wlanusermac": self.get_argument("wlanusermac","00-00-00-00-00"),
            "wlanapmac": self.get_argument("wlanapmac","00-00-00-00-00"),
            "wlanuserfirsturl": self.get_argument("wlanuserfirsturl","/portal/index"),
            "callback": self.get_argument("callback",""),
            "vendortype" : self.get_argument("vendortype",""),
        }
        logger.info(utils.safeunicode(wlan_params))
        if wlan_params['vendortype'] == 'routeros':
            logger.info("Forward to RouterOS Portal Login")
            self.forward_ros(wlan_params)
            return

        elif wlan_params['vendortype'] == 'ikuai':
            logger.info("Forward to RouterOS ikuai Login")
            self.forward_ikuai(wlan_params)
            return

        logger.info("callback_cache_%s" % utils.safeunicode(wlan_params['wlanuserip']))
        self.application.mcache.set(
            "callback_cache_%s" % utils.safestr(wlan_params['wlanuserip']),wlan_params['callback'],300)

        url = self.settings['config'].acagent.portal_login.format(**wlan_params)
        logger.info("portal forward to : %s" % url)
        self.redirect(url, permanent=False)


    def forward_ros(self, wlan_params):
        qstr = self.request.query
        ssid = wlan_params.get("ssid", "default")

        ros_action = self.get_argument("ros_action",None)

        if not ros_action:
            self.render_error(msg=u"ros_action is empty")
            return

        ispcode = wlan_params.get("ispcode", "default")
        tpl = self.get_template_attrs(ssid,ispcode)

        field_username = 'username'
        field_password = 'password'

        self.render(self.get_login_template(tpl['tpl_path']), 
            msg=None, 
            tpl=tpl, 
            qstr=qstr, 
            authurl=ros_action, 
            field_username=field_username,
            field_password=field_password,
            **wlan_params)

    def forward_ikuai(self, wlan_params):
        qstr = self.request.query
        ssid = wlan_params.get("ssid", "default")

        ikuai_action = self.get_argument("ikuai_action",None)

        if not ikuai_action:
            self.render_error(msg=u"ikuai_action is empty")
            return

        ispcode = wlan_params.get("ispcode", "default")
        tpl = self.get_template_attrs(ssid,ispcode)

        field_username = 'username'
        field_password = 'password'

        self.render(self.get_login_template(tpl['tpl_path']), 
            msg=None, 
            tpl=tpl, 
            qstr=qstr, 
            authurl=ikuai_action, 
            field_username=field_username,
            field_password=field_password,
            **wlan_params)






