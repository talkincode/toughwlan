#!/usr/bin/env python
# coding=utf-8
import msgpack
import toughwlan
from txzmq import ZmqEndpoint, ZmqFactory, ZmqPushConnection, ZmqPullConnection
from twisted.internet import protocol
from twisted.internet import reactor
from twisted.internet import defer
from toughlib import utils
from toughlib import logger
from toughwlan.radiusd.settings import *
from toughwlan.radiusd import auth_worker
from toughwlan.radiusd import acct_worker


class RADIUSMaster(protocol.DatagramProtocol):
    def __init__(self, config, service='auth'):
        self.config = config
        self.service = service
        self.pusher = ZmqPushConnection(ZmqFactory(), ZmqEndpoint('bind', 'ipc:///tmp/twradiusd-%s-message' % service))
        self.puller = ZmqPullConnection(ZmqFactory(), ZmqEndpoint('bind', 'ipc:///tmp/twradiusd-%s-result' % service))
        self.puller.onPull = self.reply

    def datagramReceived(self, datagram, (host, port)):
        message = msgpack.packb([datagram, host, port])
        self.pusher.push(message)
        
    def reply(self, result):
        data, host, port = msgpack.unpackb(result[0])
        self.transport.write(data, (host, int(port)))



def run_auth(config):
    auth_protocol = RADIUSMaster(config, service='auth')
    reactor.listenUDP(int(config.radiusd.auth_port), auth_protocol, interface=config.radiusd.host)

def run_acct(config):
    acct_protocol = RADIUSMaster(config,service='acct')
    reactor.listenUDP(int(config.radiusd.acct_port), acct_protocol, interface=config.radiusd.host)

def run_worker(config,dbengine):
    auth_worker.RADIUSAuthWorker(config,dbengine)
    acct_worker.RADIUSAcctWorker(config,dbengine)
    logger.info('start radius worker')


