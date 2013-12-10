#!/usr/bin/python

from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver
from CommonUtils import Caller


class FritzboxClientFactory(ReconnectingClientFactory):
    initialDelay = 20
    maxDelay = 30
    hangup_ok = False
    def __init__(self, onCallIncoming=None):
        self.onCallIncoming = onCallIncoming

    def startedConnecting(self, connector):
        print("Connecting to Fritzbox Callmonitor...")

    def clientConnectionLost(self, connector, reason):
        print("Connection to Fritzbox Callmonitor lost\n (%s)\nretrying..." % reason.getErrorMessage())
        if not self.hangup_ok:
            ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print("Connecting to Fritzbox Callmonitor failed\n (%s)\nretrying..." % reason.getErrorMessage())
        if not self.hangup_ok:
            ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def buildProtocol(self, addr):
        return FritzboxLineReceiver(self.onCallIncoming)


class FritzboxLineReceiver(LineReceiver):
    def __init__(self, onCallIncoming):
        self.onCallIncoming = onCallIncoming
        self.resetValues()

    def resetValues(self):
        self.number = None
        self.caller = None
        self.date = '01011970'
        self.time = '0001'
        self.line = ''
        self.event = None

    def lineReceived(self, line):
        print("[FritzboxLineReceiver] lineReceived: %s" % line)

        # b'21.11.13 22:36:08;RING;0;01606685404;3005988;SIP0;'
        # b'21.11.13 22:36:15;DISCONNECT;0;0;'
        self.line = line
        items = line.decode("utf-8").split(";")
        if items[1] == "RING":
            self.date = items[0]
            self.event = items[1]
            self.number = items[3]

            # TODO Lookup
            self.caller = "Unkown"

            self.onCallIncoming(Caller(self.number, self.number))


class FritzboxClient():
    def __init__(self, hostname, onCallIncoming=None):
        self.onCallIncoming = onCallIncoming
        self.hostname = hostname
        self.port = 1012
        self.desc = None
        self.connect()

    def connect(self):
        self.abort()
        factory = FritzboxClientFactory(self.onCallIncoming)
        self.desc = (factory, reactor.connectTCP(self.hostname, self.port, factory))

    def shutdown(self):
        self.abort()

    def abort(self):
        if self.desc is not None:
            self.desc[0].hangup_ok = True
            self.desc[0].stopTrying()
            self.desc[1].disconnect()
            self.desc = None
