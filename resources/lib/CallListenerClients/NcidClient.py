#!/usr/bin/python

from zope.interface import implements
from CallListenerClients import IClient


class NcidClient:
    implements(IClient)

    def __init__(self):
        self.dialog = None
        self.desc = None
        if config.plugins.NcidClient.enable.value:
            self.connect()

    def connect(self):
        self.abort()
        if config.plugins.NcidClient.enable.value:
            factory = NcidClientFactory()
            self.desc = (factory, reactor.connectTCP(config.plugins.NcidClient.hostname.value,
                                                     config.plugins.NcidClient.port.value, factory))

    def shutdown(self):
        self.abort()

    def abort(self):
        if self.desc is not None:
            self.desc[0].hangup_ok = True
            self.desc[0].stopTrying()
            self.desc[1].disconnect()
            self.desc = None