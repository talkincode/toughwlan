#!/usr/bin/env python
# coding=utf-8
import uuid
import time
from txradius.radius import packet
from twisted.internet import defer
from twisted.internet import task
from twisted.python import log
from twisted.internet import reactor
from txradius import message

class RadiusSession:

    sessions = {}

    def __init__(self, config, radius, log=log):
        self.config = config
        self.radius = radius
        self.log=log
        self.session_start = int(time.time())
        self.session_id = uuid.uuid1().hex.upper()
        self.session_data = {}
        self.interim_update = self.config.acagent.radius.interim_update

    @staticmethod
    def find_session(ipaddr):
        return (s for s in RadiusSession.sessions.itervalues() if s.session_data['Framed-IP-Address'] == ipaddr)


    @defer.inlineCallbacks
    def start(self, username, password, challenge=None, chap_pwd=None, userip=None, usermac=None):
        auth_req = {'User-Name' : username}
        auth_req["NAS-IP-Address"]     =  self.config.acagent.nasaddr
        auth_req["NAS-Port"]           = 0
        auth_req["Service-Type"]       = "Login-User"
        auth_req["NAS-Identifier"]     = "toughac"
        auth_req["Called-Station-Id"]  = usermac or "00-00-00-00-00-00"
        auth_req["Framed-IP-Address"]  =  userip
        auth_resp = {}
        if challenge and chap_pwd:
            auth_req['CHAP-Challenge'] = challenge
            auth_req['CHAP-Password'] = chap_pwd
            auth_resp = yield self.radius.send_auth(**auth_req)
        else:
            auth_req['User-Password'] = password
            auth_resp = yield self.radius.send_auth(**auth_req)

        if auth_resp.code== packet.AccessReject:
            defer.returnValue(dict(code=1, msg=auth_resp.get("Reply-Message", "auth reject")))

        if auth_resp.code== packet.AccessAccept:
            self.session_data['User-Name'] = username
            self.session_data['Acct-Session-Time'] = 0
            self.session_data['Acct-Status-Type'] = 1
            self.session_data['Session-Timeout'] = message.get_session_timeout(auth_resp)
            self.session_data['Acct-Session-Id'] = self.session_id
            self.session_data["NAS-IP-Address"]     =  self.config.acagent.nasaddr
            self.session_data["NAS-Port"]           = 0
            self.session_data["NAS-Identifier"]     = self.config.acagent.nasid
            self.session_data["Called-Station-Id"]  = usermac or "00-00-00-00-00-00"
            self.session_data["Framed-IP-Address"]  =  userip
            self.session_data["Acct-Output-Octets"]  =  0
            self.session_data["Acct-Input-Octets"]  =  0
            self.session_data["NAS-Port-Id"]  =  '3/0/1:0.0'
            if 'Acct-Interim-Interval' in auth_resp:
                self.interim_update = message.get_interim_update(auth_resp)

            acct_resp = yield self.radius.send_acct(**self.session_data)
            if acct_resp.code == packet.AccountingResponse:
                self.log.msg('Start session  %s' % self.session_id)
                RadiusSession.sessions[self.session_id] = self
                reactor.callLater(self.interim_update,self.check_session)
                defer.returnValue(dict(code=0,msg=u"success"))
            else:
                defer.returnValue(dict(code=1,msg=u"error"))

    @defer.inlineCallbacks
    def update(self):
        self.log.msg('Alive session  %s' % self.session_id)
        self.session_data['Acct-Status-Type'] = 3
        self.session_data['Acct-Session-Time'] = (int(time.time()) - self.session_start)
        acct_resp = yield self.radius.send_acct(**self.session_data)
        defer.returnValue(acct_resp)

    @defer.inlineCallbacks
    def stop(self):
        self.log.msg('Stop session  %s' % self.session_id)
        del RadiusSession.sessions[self.session_id]
        self.session_data['Acct-Status-Type'] = 2
        self.session_data['Acct-Session-Time'] = (int(time.time()) - self.session_start)
        acct_resp = yield self.radius.send_acct(**self.session_data)
        defer.returnValue(acct_resp)

    def check_session(self):
        session_time = int(time.time()) - self.session_start
        if session_time > self.session_data['Session-Timeout']:
            self.stop().addCallbacks(self.log.msg,self.log.err)
        else:
            self.update().addCallbacks(self.log.msg,self.log.err)
            reactor.callLater(self.interim_update,self.check_session)



























