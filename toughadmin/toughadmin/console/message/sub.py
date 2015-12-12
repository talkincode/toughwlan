#!/usr/bin/env python
#coding=utf-8

from twisted.internet.protocol import Protocol, ClientFactory
from sys import stdout


class Echo(Protocol):
    def connectionMade(self):
        self.transport.write("nas")

    def dataReceived(self, data):
        stdout.write(data)


class EchoClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        return Echo()

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason


from twisted.internet import reactor

reactor.connectTCP("127.0.0.1", 1025, EchoClientFactory())
reactor.run()