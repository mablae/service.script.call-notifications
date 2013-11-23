#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet import reactor, defer
from twisted.internet.protocol import Factory, Protocol

from CommonUtils import Caller, Event


class YacProtocol(Protocol):
    def __init__(self, callback):
        self.fireEvent = Event()
        self.fireEvent += callback

    def dataReceived(self, data):
        """
        As soon as any data transform it to data
        """
        print("Looks like some YAC data coming in:'%s'..." % data)
        self.result = None
        self.buffer = (data[5:].split("~"))
        if len(self.buffer) > 1:
            self.result = Caller(self.buffer[0], self.buffer[1])
            self.fireEvent(self.result)

    def connectionLost(self, reason):
        """
        As soon as the client disconnects we log that
        """
        print("The client closed the YAC connection")


class YacServerFactory(Factory):
    fireMe = Event()
    def __init__(self, callback):
        self.callback = callback


    def buildProtocol(self, addr):
        return YacProtocol(self.callback)

class YacServer:
    def __init__(self, listen_port, callback):
        self.listen_port = int(listen_port)
        self.desc = None
        self.callback = callback
        # TODO: add check for enabled setting

    def start(self):
        f = YacServerFactory(self.callback)
        # TODO: add check for enabled setting
        self.desc = (f, reactor.listenTCP(self.listen_port, f))

    def shutdown(self):
        self.abort()

    def abort(self):
        print("Closing Server")
        if self.desc is not None:
            self.desc[0].hangup_ok = True
            #self.desc[0].stopTrying()
            #self.desc[1].disconnect()
            self.desc = None