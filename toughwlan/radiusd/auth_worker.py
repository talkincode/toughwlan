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


class RADIUSAuthWorker(RADIUSWorker):

    def __init__(self, config, dbengine):
        RADIUSWorker.__init__(self,config, dbengine)
        self.pusher = ZmqPushConnection(ZmqFactory(), ZmqEndpoint('connect', 'ipc:///tmp/twradiusd-auth-result'))
        self.puller = ZmqPullConnection(ZmqFactory(), ZmqEndpoint('connect', 'ipc:///tmp/twradiusd-auth-message'))
        self.puller.onPull = self.process

    @defer.inlineCallbacks
    def process(self, message):
        datagram, host, port =  msgpack.unpackb(message[0])
        reply = yield self.processAuth(datagram, host, port)
        if reply is None:
            return
        logger.info("[Radiusd] :: Send auth radius response: %s" % repr(reply))
        if self.config.system.debug:
            logger.debug(reply.format_str())
        self.pusher.push(msgpack.packb([reply.ReplyPacket(),host,port]))

    def createAuthPacket(self, **kwargs):
        vendor_id = kwargs.pop('vendor_id',0)
        auth_message = message.AuthMessage(**kwargs)
        auth_message.vendor_id = vendor_id
        auth_message = mac_parse.process(auth_message)
        return auth_message

    @defer.inlineCallbacks
    def processAuth(self, datagram, host, port):
        try:
            bas = self.find_nas(host)
            if not bas:
                raise PacketError('[Radiusd] :: Dropping packet from unknown host %s' % host)

            secret, vendor_id = bas['bas_secret'], bas['vendor_id']
            req = self.createAuthPacket(packet=datagram, 
                dict=self.dict, secret=six.b(str(secret)),vendor_id=vendor_id)

            logger.info("[Radiusd] :: Received radius request: %s" % (repr(req)))
            if self.config.system.debug:
                logger.debug(req.format_str())

            if req.code != packet.AccessRequest:
                raise PacketError('non-AccessRequest packet on authentication socket')

            reply = req.CreateReply()
            reply.vendor_id = req.vendor_id

            account = self.find_account(req.get_user_name())
            if not account:
                reply['Reply-Message'] = u"user not exsts"
                reply.code = packet.AccessReject
                defer.returnValue(reply) 
            
            if self.config.radiusd.bypass == 0:
                is_pwd_ok = True
            else:
                is_pwd_ok = req.is_valid_pwd(self.aes.decrypt(account.password))

            if not is_pwd_ok:
                reply['Reply-Message'] =  "password not match"
                reply.code = packet.AccessReject
                defer.returnValue(reply) 
            
            reply = rate_process.process(reply, input_rate=account.input_rate, output_rate=account.output_rate)

            attrs = self.find_account_attrs(req.get_user_name())
            for attr in attrs:
                try:
                    # todo: May have a type matching problem
                    reply.AddAttribute(utils.safestr(attr.attr_name), attr.attr_value)
                except Exception as err:
                    errstr = "RadiusError:current radius cannot support attribute {0},{1}".format(
                        attr.attr_name,utils.safestr(err.message))
                    logger.error(errstr)

            reply['Reply-Message'] = 'success!'
            reply.code = packet.AccessAccept
            if not req.VerifyReply(reply):
                raise PacketError('VerifyReply error')
            defer.returnValue(reply) 
        except Exception as err:
            errstr = 'RadiusError:Dropping invalid auth packet from {0} {1},{2}'.format(
                host, port, utils.safeunicode(err))
            logger.error(errstr)
            import traceback
            traceback.print_exc()

