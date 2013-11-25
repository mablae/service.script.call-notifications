#!/usr/bin/env python

from twisted.internet import reactor
from twisted.internet import task
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

def parseBoolString(theString):
  return theString[0].upper()=='T'

def handleIncomingCall(caller):
    if caller.caller == "Unknown":
        caller.caller = xbmcaddon.getLocalizedString(30602)
    xbmcDialog.notification(xbmcAddon.getLocalizedString(30601) % caller.caller, caller.number)


def initServices():
    #xbmc.log('initServices() running...', xbmc.LOGDEBUG)

    if parseBoolString(xbmcAddon.getSetting("server.yac.enabled")):
        xbmc.log("Starting YAC Server ", xbmc.LOGDEBUG)
        serverPool['yac'] = YacServer(int(xbmcAddon.getSetting("server.yac.listen_port")), handleIncomingCall)
        serverPool['yac'].start()

    if parseBoolString(xbmcAddon.getSetting("client.fritzbox.enabled")):
        #xbmc.log("Starting Fritzbox Client", xbmc.LOGDEBUG)
        clientPool['fritzbox'] = FritzboxClient(xbmcAddon.getSetting("client.fritzbox.host"), handleIncomingCall)


def bootServices():
    initServices()

    # TODO Emulate SIGTERM inside XBMC in correct way
    l = task.LoopingCall(shouldWeExit)
    l.start(0.5)

    reactor.run(installSignalHandlers=0)


def shouldWeExit():
    if xbmc.abortRequested == True:
        xbmc.log("shouldWeExit() - Indeed, we better stop reactor now...", xbmc.LOGDEBUG)
        reactor.stop()
        sys.exit()


if __name__ == "__main__":
    bootServices()
