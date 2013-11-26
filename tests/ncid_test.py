#!/usr/bin/env python

import sys

from twisted.internet import reactor
from twisted.python import log

from CallListenerClients.NcidClient import NcidClient


log.startLogging(sys.stdout)

def handleIncomingCall(caller):
    print "handleIncomingCall"
    print caller

ncidClient = NcidClient(onCallIncoming=handleIncomingCall)
reactor.run()