#!/usr/bin/env python
# coding=utf-8
from hashlib import md5
import json
import time

from twisted.internet import defer

from toughengine.common import requests,logger
from toughengine.radiusd.utils import safestr


class HttpClient():
    """
    RestFull Client
    :param config:
    :type config:
    """

    def __init__(self, config):
        self.config = config
        self.log = logger.Logger(self.config)

    def make_sign(self, secret, params=[]):
        """ make sign
        :param secret:
        :param params: params list
        :return: :rtype:
        """
        _params = [safestr(p) for p in params if p is not None]
        _params.sort()
        _params.insert(0, secret)
        strs = safestr(''.join(_params))
        # if self.config.defaults.debug:
        #     self.log.info("[HttpClient] ::::::: sign_src = %s" % strs)
        mds = md5(strs).hexdigest()
        return mds.upper()

    def check_sign(self, secret, msg):
        """ check message sign
        :param secret:
        :param msg: dict type  data
        :return: :rtype: boolean
        """
        if "sign" not in msg:
            return False
        sign = msg['sign']
        params = [msg[k] for k in msg if k != 'sign' ]
        local_sign = self.make_sign(secret, params)
        # if self.config.defaults.debug:
        #     self.log.msg("[HttpClient] ::::::: remote_sign = %s ,local_sign = %s" % (sign, local_sign))
        return sign == local_sign


    @defer.inlineCallbacks
    def send(self,apiurl,reqdata,secret):
        """ send radius request
        :param apiurl: oss server api
        :param reqdata: json data
        """
        try:
            if self.config.defaults.debug:
                self.log.msg("[HttpClient] ::::::: Send http request to {0}, {1}".format(safestr(apiurl),safestr(reqdata)))

            headers = {"Content-Type": ["application/json;charset=utf-8"]}
            resp = yield requests.post(safestr(apiurl), data=reqdata, headers=headers)
            resp_json = yield resp.json()

            if self.config.defaults.debug:
                self.log.msg("[HttpClient] ::::::: Received http response from {0}, {1}".format(safestr(apiurl), safestr(resp_json)))

            if resp.code != 200:
                defer.returnValue(dict(code=1, msg=u'server return error http status code {0}'.format(resp.code)))
            else:
                result = resp_json
                if not self.check_sign(secret, result):
                    defer.returnValue(dict(code=1, msg=u"sign error"))
                else:
                    defer.returnValue(result)
        except Exception as err:
            import traceback
            traceback.print_exc()
            defer.returnValue(dict(code=1, msg=u'server error'))

    @defer.inlineCallbacks
    def get_nas(self, nasaddr):
        nas_fetch_url = self.config.radiusd.get('nas_fetch_url')
        nas_fetch_secret = self.config.radiusd.get('nas_fetch_secret')
        if not nas_fetch_url:
            raise ValueError("nas_fetch_url is None")

        try:
            nonce = str(time.time())
            sign = self.make_sign(nas_fetch_secret,params=[nasaddr, nonce])
            reqdata = json.dumps(dict(
                nasaddr=nasaddr,
                nonce=nonce,
                sign=sign
            ), ensure_ascii=False)
            resp = yield self.send(nas_fetch_url, reqdata, nas_fetch_secret)
            print resp
            defer.returnValue(resp)
        except Exception as err:
            import traceback
            traceback.print_exc()
            self.log.msg(u"[HttpClient] ::::::: fetch nas failure,%s" % safestr(err.message))
            defer.returnValue(dict(code=1, msg=u"fetch nas error, please see log detail"))



    @defer.inlineCallbacks
    def authorize(self, username, domain, macaddr, nasaddr, vlanid1, vlanid2, textinfo=None):
        """send radius auth request
        :param username: not contain @doamin
        :param domain:
        :param macaddr:
        :param nasaddr:
        :param vlanid1:
        :param vlanid2:
        :param textinfo:
        """
        try:
            nas = yield self.get_nas(nasaddr)
            nonce = str(time.time())
            sign = self.make_sign(nas.get("api_secret"), [username, domain, macaddr, nasaddr, vlanid1, vlanid2, textinfo, nonce])
            apiurl = nas and nas.get("api_auth_url") or None
            reqdata = json.dumps(dict(
                username=username,
                domain=safestr(domain),
                macaddr=safestr(macaddr),
                nasaddr=nasaddr,
                vlanid1=vlanid1,
                vlanid2=vlanid2,
                textinfo=safestr(textinfo),
                nonce=nonce,
                sign=sign
            ), ensure_ascii=False)
            resp = yield self.send(apiurl, reqdata, nas.get("api_secret"))
            defer.returnValue(resp)
        except Exception as err:
            self.log.msg(u"[HttpClient] ::::::: authorize failure,%s" % safestr(err.message))
            defer.returnValue(dict(code=1, msg=u"authorize error, please see log detail"))

    @defer.inlineCallbacks
    def accounting(self,req_type,username, session_id, session_time,session_timeout,macaddr,nasaddr,ipaddr,
                   input_octets,output_octets,input_pkts,output_pkts, textinfo=None):
        """send radius accounting request
        :param req_type: 1 Start 2 Stop 3 Alive
        :param username:
        :param session_id:
        :param session_time:
        :param session_timeout:
        :param macaddr:
        :param nasaddr:
        :param ipaddr:
        :param input_octets:
        :param output_octets:
        :param input_pkts:
        :param output_pkts:
        :param textinfo:
        """
        try:
            nas = yield self.get_nas(nasaddr)
            nonce = str(time.time())
            sign = self.make_sign(nas.get("api_secret"), [req_type, username, session_id, session_time, session_timeout, macaddr, nasaddr, ipaddr,
                                input_octets, output_octets, input_pkts, output_pkts,nonce])

            apiurl = nas and nas.get("api_acct_url") or None
            reqdata = json.dumps(dict(
                req_type=req_type,
                username=username,
                session_id=session_id,
                session_time=session_time,
                session_timeout=session_timeout,
                macaddr=macaddr,
                nasaddr=nasaddr,
                ipaddr=ipaddr,
                input_octets=input_octets,
                output_octets=output_octets,
                input_pkts=input_pkts,
                output_pkts=output_pkts,
                textinfo=safestr(textinfo),
                nonce=nonce,
                sign=sign
            ), ensure_ascii=False)
            resp = yield self.send(apiurl, reqdata, nas.get("api_secret"))
            defer.returnValue(resp)
        except Exception as err:
            self.log.msg(u"[HttpClient] ::::::: accounting failure,%s" % safestr(err.message))
            defer.returnValue(dict(code=1, msg=u"accounting error, please see log detail"))



