#!/usr/bin/python 


from CallListenerClients.AbstractClient import AbstractClient
from CallListenerClients.FritzboxClientFactory import FritzboxClientFactory

from twisted.internet import reactor


class FritzboxClient():
        def __init__(self, hostname, port=1012):
            self.hostname = hostname
            self.port = port
            self.desc = None
            # TODO: add check for enabled setting
            self.connect()

        def connect(self):
                self.abort()
                # TODO: add check for enabled setting
                factory = FritzboxClientFactory()
                self.desc = (factory, reactor.connectTCP(self.hostname, self.port, factory))

        def shutdown(self):
                self.abort()

        def abort(self):
                if self.desc is not None:
                        self.desc[0].hangup_ok = True
                        self.desc[0].stopTrying()
                        self.desc[1].disconnect()
                        self.desc = None
