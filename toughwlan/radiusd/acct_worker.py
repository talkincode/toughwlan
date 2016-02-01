#!/usr/bin/env python
# coding=utf-8
import datetime
import os
import six
import msgpack
import toughwlan
from txzmq import ZmqEndpoint, ZmqFactory, ZmqPushConnection, ZmqPullConnection
from twisted.internet import reactor
from twisted.internet import defer
from toughlib import utils
from toughlib import logger
from toughlib import db_cache as cache
from txradius.radius import dictionary
from txradius.radius import packet
from txradius.radius.packet import PacketError
from txradius.ext import mac_parse, rate_process
from txradius import message
from toughlib.utils import timecast
from toughlib.storage import Storage
from toughwlan.radiusd.settings import *
from toughwlan.radiusd.basic_worker import RADIUSWorker
from toughwlan import models

class RADIUSAcctWorker(RADIUSWorker):

    def __init__(self, config, dbengine):
        RADIUSWorker.__init__(self,config, dbengine)
        self.pusher = ZmqPushConnection(ZmqFactory(), ZmqEndpoint('connect', 'ipc:///tmp/twradiusd-acct-result'))
        self.puller = ZmqPullConnection(ZmqFactory(), ZmqEndpoint('connect', 'ipc:///tmp/twradiusd-acct-message'))
        self.puller.onPull = self.process

    @defer.inlineCallbacks
    def process(self, message):
        datagram, host, port =  msgpack.unpackb(message[0])
        reply = yield self.processAcct(datagram, host, port)
        if reply is None:
            return
        logger.info("[Radiusd] :: Send acct radius response: %s" % repr(reply))
        if self.config.system.debug:
            logger.debug(reply.format_str())
        self.pusher.push(msgpack.packb([reply.ReplyPacket(),host,port]))


    def createAcctPacket(self, **kwargs):
        vendor_id = 0
        if 'vendor_id' in kwargs:
            vendor_id = kwargs.pop('vendor_id')
        acct_message = message.AcctMessage(**kwargs)
        acct_message.vendor_id = vendor_id
        acct_message = mac_parse.process(acct_message)
        return acct_message


    @defer.inlineCallbacks
    def processAcct(self, datagram, host, port):
        try:
            bas = self.find_nas(host)
            if not bas:
                raise PacketError('[Radiusd] :: Dropping packet from unknown host %s' % host)

            secret, vendor_id = bas['bas_secret'], bas['vendor_id']
            req = self.createAcctPacket(packet=datagram, 
                dict=self.dict, secret=six.b(str(secret)),vendor_id=vendor_id)

            logger.info("[Radiusd] :: Received radius request: %s" % (repr(req)))
            if self.config.system.debug:
                logger.debug(req.format_str())

            if req.code != packet.AccountingRequest:
                raise PacketError('non-AccountingRequest packet on authentication socket')

            if not req.VerifyAcctRequest():
                raise PacketError('VerifyAcctRequest error')

            status_type = req.get_acct_status_type()
            if status_type == STATUS_TYPE_START:
                self.start_online(req.get_ticket())
            elif status_type == STATUS_TYPE_UPDATE:
                self.update_online(req.get_ticket())
            elif status_type == STATUS_TYPE_UPDATE:
                self.stop_online(req.get_ticket())

            defer.returnValue(req.CreateReply()) 
        except Exception as err:
            errstr = 'RadiusError:Dropping invalid acct packet from {0} {1},{2}'.format(
                host, port, utils.safeunicode(err))
            logger.error(errstr)
            import traceback
            traceback.print_exc()

    @timecast
    def start_online(self,ticket):
        if self.is_online(ticket['nas_addr'],ticket['acct_session_id']):
            return logger.error('online %s is exists' % ticket['acct_session_id'])

        if not self.find_account(ticket['account_number']):
            return logger.error('user %s not exists' % ticket['account_number'])

        online = Storage(
            account_number = ticket['account_number'],
            nas_addr = ticket['nas_addr'],
            session_id = ticket['acct_session_id'],
            start_time = datetime.datetime.now().strftime( "%Y-%m-%d %H:%M:%S"),
            ipaddr = ticket['framed_ipaddr'],
            mac_addr = ticket['mac_addr'],
            nas_port_id = ticket['nas_port_id'],
            input_total = 0,
            output_total = 0
        )
        self.add_online(online)
        logger.info('%s Accounting start request, add new online'%online.account_number)

    @timecast
    def update_online(self,ticket):
        if not self.find_account(ticket['account_number']):
            return logger.error('user %s not exists' % ticket['account_number'])

        online = self.get_online(ticket['nas_addr'],ticket['acct_session_id'])     
        if not online:         
            sessiontime = ticket['acct_session_time']
            updatetime = datetime.datetime.now()
            _starttime = updatetime - datetime.timedelta(seconds=sessiontime)       
            online = Storage(
                account_number = ticket['account_number'],
                nas_addr = ticket['nas_addr'],
                session_id = ticket['acct_session_id'],
                start_time = _starttime.strftime( "%Y-%m-%d %H:%M:%S"),
                ipaddr = ticket['framed_ipaddr'],
                mac_addr = ticket['mac_addr'],
                nas_port_id = ticket['nas_port_id'],
                input_total = self.get_input_total(ticket),
                output_total = self.get_output_total(ticket)
            )
            self.add_online(online)
        logger.info('%s Accounting update request, update online'% ticket['account_number'])

    @timecast
    def stop_online(self,ticket):
        self.del_online(ticket['nas_addr'],ticket['acct_session_id'])
        logger.info('%s Accounting stop request, remove online'% ticket['account_number'])



