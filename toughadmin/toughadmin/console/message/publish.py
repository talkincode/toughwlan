#!/usr/bin/env python
#coding=utf-8

from twisted.internet import reactor, protocol, endpoints

class Client:

    def __init__(self, conn, topic=None):
        self.topic = topic
        self.conn = conn

    def push(self, data):
        self.conn.write(data)


class PubProtocol(protocol.ProcessProtocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.client = Client(self.transport)
        self.factory.clients.add(self.client)
        print "add %s" % self.client

    def connectionLost(self, reason):
        print "remove %s" % self.client
        self.factory.clients.remove(self.client)

    def dataReceived(self, data):
        print data
        for c in self.factory.clients:
            c.push(data)


class PubFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return PubProtocol(self)


endpoints.serverFromString(reactor, "tcp:1025").listen(PubFactory())
reactor.run()