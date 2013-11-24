#!/usr/bin/env python

from twisted.internet import reactor
import sys
from CallListenerClients.FritzboxClient import FritzboxClient
from Yac.YacServer import YacServer

runningOutsideXbmc = False
try:
    import xbmc, xbmcgui, xbmcaddon
except ImportError, e:
    print "Could not find xbmc modules!"
    sys.exit()


clientPool = {}
serverPool = {}
resolverPool = {}

xbmcAddon = xbmcaddon.Addon()
xbmcDialog = xbmcgui.Dialog()

def handleIncomingCall(Caller):
    print "Iam into it:..!"

def initServices():
    print("Init services...")

    serverPool['yac'] = YacServer(10629, handleIncomingCall)
    serverPool['yac'].start()

    clientPool['fritzbox'] = FritzboxClient("192.168.178.1", handleIncomingCall)

def bootServices():
    initServices()
    reactor.run(installSignalHandlers=0)


if __name__ == "__main__":
    bootServices()
