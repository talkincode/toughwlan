#!/usr/bin/env python
# coding:utf-8
import cyclone.auth
import cyclone.escape
import cyclone.httpclient as httpclient
import cyclone.web
from toughadmin.console.handlers.base import BaseHandler, MenuUser
from toughadmin.common.permit import permit
import urllib
from toughadmin.console import models
from twisted.internet import defer
from twisted.python import log
import json
from hashlib import md5

def mksign(secret, params=[]):
    _params = [str(p) for p in params if p is not None]
    _params.sort()
    _params.insert(0, secret)
    strs = ''.join(_params)
    log.msg("sign_src = %s" % strs)
    mds = md5(strs.encode()).hexdigest()
    return mds.upper()


@permit.route(r"/user/packets", u"用户消息查询", MenuUser, order=2.1000, is_menu=True)
class UserPacketsHandler(BaseHandler):


    @cyclone.web.authenticated
    def get(self):
        self.render("userPackets.html")

    @defer.inlineCallbacks
    def post(self):
        headers = {"Content-type": ["application/x-www-form-urlencoded"]}
        username = self.get_argument("username")

        params = [username]

        sign = mksign(self.settings.config.defaults.secret, params)

        post_data={"userName":username,"sign":sign}
        body = urllib.urlencode(post_data)

        radius_list = self.db.query(models.TraRadius).all()

        packets = []

        for radius in radius_list:
            try:
                resp = yield httpclient.fetch("http://%s:1815/api/queryPacketRecord" %radius.ip_addr, postdata=body, headers=headers)
                resp_msg = json.loads(resp.body)
                packets.extend(resp_msg.get('data') or [])
                log.msg(u'%s recieve a response ' %radius.ip_addr)
            except Exception, e:
                import traceback
                log.msg(u'%s cannot recieve a response, check this radius client please' %radius.ip_addr)
                traceback.print_exc()
        log.msg(username + u' recently message' + unicode(packets))
        self.render("userPackets.html",packets=packets)


