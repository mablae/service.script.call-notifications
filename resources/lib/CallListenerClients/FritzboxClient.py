#!/usr/bin/python

from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver
from CommonUtils import Caller


class FritzboxClientFactory(ReconnectingClientFactory):
    initialDelay = 20
    maxDelay = 30

    def __init__(self, callback):
        self.callback = callback

    def startedConnecting(self, connector):
        print("Connecting to Fritzbox Callmonitor...")
        # TODO
        #if config.plugins.NcidClient.connectionVerbose.value:
        #        Notifications.AddNotification(MessageBox, _("Connecting to NCID Server..."), type=MessageBox.TYPE_INFO, timeout=2)

    def clientConnectionLost(self, connector, reason):
        #global ncidsrv
        print("Connection to Fritzbox Callmonitor lost\n (%s)\nretrying..." % reason.getErrorMessage())
        #if not self.hangup_ok and config.plugins.NcidClient.connectionVerbose.value:
        #        Notifications.AddNotification(MessageBox, _("Connection to NCID Server lost\n (%s)\nretrying...") % reason.getErrorMessage(), type=MessageBox.TYPE_INFO, timeout=config.plugins.NcidClient.timeout.value)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
        # config.plugins.NcidClient.enable.value = False
        ncidsrv = None

    def clientConnectionFailed(self, connector, reason):
        #global ncidsrv
        print("Connecting to Fritzbox Callmonitor failed\n (%s)\nretrying..." % reason.getErrorMessage())
        #if config.plugins.NcidClient.connectionVerbose.value:
        #        Notifications.AddNotification(MessageBox, _("Connecting to NCID Server failed\n (%s)\nretrying...") % reason.getErrorMessage(), type=MessageBox.TYPE_INFO, timeout=config.plugins.NcidClient.timeout.value)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
        # config.plugins.NcidClient.enable.value = False
        #ncidsrv = None

    def buildProtocol(self, addr):
        return FritzboxLineReceiver(self.callback)


class FritzboxLineReceiver(LineReceiver):
    def __init__(self, callback):
        self.callback = callback
        self.resetValues()

    def resetValues(self):
        self.number = None
        self.caller = None
        self.date = '01011970'
        self.time = '0001'
        self.line = ''
        self.event = None

    def notify(self):
        print("notifyCall(" + self.date + "," + self.number + "," + self.caller + ")")
        self.resetValues()

    def lineReceived(self, line):
        print("[FritzboxLineReceiver] lineReceived: %s" % line)

        # b'21.11.13 22:36:08;RING;0;01606685404;3005988;SIP0;'
        # b'21.11.13 22:36:15;DISCONNECT;0;0;'
        self.line = line
        items = line.decode("utf-8").split(";")

        self.date = items[0]
        self.event = items[1]
        self.number = items[3]

        # TODO Lookup
        self.caller = "Unkown"

        self.callback(Caller(self.number, self.number))


class FritzboxClient():
    def __init__(self, hostname, callback):
        self.callback = callback
        self.hostname = hostname
        self.port = 1012
        self.desc = None
        self.connect()

    def connect(self):
        self.abort()
        factory = FritzboxClientFactory(self.callback)
        self.desc = (factory, reactor.connectTCP(self.hostname, self.port, factory))

    def shutdown(self):
        self.abort()

    def abort(self):
        if self.desc is not None:
            self.desc[0].hangup_ok = True
            self.desc[0].stopTrying()
            self.desc[1].disconnect()
            self.desc = None
