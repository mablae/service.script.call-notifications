#!/usr/bin/env python

from CallListenerClients.FritzboxClient import FritzboxClient
from twisted.internet import reactor



fbClient = FritzboxClient("192.168.178.1")
reactor.run()