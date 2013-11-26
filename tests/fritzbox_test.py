#!/usr/bin/env python


import sys
from CallListenerClients.FritzboxClient import FritzboxClient
from twisted.internet import reactor
from twisted.python import log


log.startLogging(sys.stdout)

def handleIncomingCall(caller):
    print "handleIncomingCall"
    print caller


fbClient = FritzboxClient("192.168.178.1", onCallIncoming=handleIncomingCall)
reactor.run()