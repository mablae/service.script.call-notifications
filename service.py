#!/usr/bin/env python

import sys, os, json

from twisted.internet import reactor
from twisted.internet import task

from CallListenerClients.FritzboxClient import FritzboxClient
from CallListenerClients.NcidClient import NcidClient
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

notificationTimeout = int(int(xbmcAddon.getSetting("notification.duration"))*1000)
notificationIcon = os.path.join(xbmcAddon.getAddonInfo("path"), "resources", "media", "icon_ring.png")


def parseBoolString(theString):
    return theString[0].upper() == 'T'


def handleIncomingCall(caller):

    if caller.caller == "Unknown":
        caller.caller = xbmcaddon.getLocalizedString(30602)

    xbmc.executebuiltin("XBMC.Notification(%s,%s,%s,%s)" % (xbmcAddon.getLocalizedString(30601) % caller.caller,
                                                            caller.number,
                                                            int(notificationTimeout),
                                                            notificationIcon
                                                            ))

    activePlayers = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}'))


    if parseBoolString(xbmcAddon.getSetting("general.pause_playback.enabled")):
        for player in activePlayers["result"]:
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.PlayPause", "params": { "playerid": %s, "play": false }, "id": 1}' % player["playerid"])

    if parseBoolString(xbmcAddon.getSetting("general.lower_volume.enabled")):
        targetVolume = int(xbmcAddon.getSetting("general.lower_volume.to"))
        currentVolume = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Application.GetProperties", "params": { "properties": ["volume"] }, "id": 1}'))
        if int(currentVolume["result"]["volume"]) >= targetVolume:
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Application.SetVolume", "params": { "volume": %s }, "id": 1}' % targetVolume)

    if parseBoolString(xbmcAddon.getSetting("general.mute_volume.enabled")):
        mutedState  = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Application.GetProperties", "params": { "properties": ["muted"] }, "id": 1}'))
        if not mutedState['result']['muted']:
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Application.SetMute", "params": { "mute": true }, "id": 1}')



def initServices():
    if parseBoolString(xbmcAddon.getSetting("server.yac.enabled")):
        xbmc.log("Starting YAC Server ", xbmc.LOGDEBUG)
        serverPool['yac'] = YacServer(int(xbmcAddon.getSetting("server.yac.listen_port")), handleIncomingCall)
        serverPool['yac'].start()

    if parseBoolString(xbmcAddon.getSetting("client.fritzbox.enabled")):
        #xbmc.log("Starting Fritzbox Client", xbmc.LOGDEBUG)
        clientPool['fritzbox'] = FritzboxClient(xbmcAddon.getSetting("client.fritzbox.host"), handleIncomingCall)

    if parseBoolString(xbmcAddon.getSetting("client.ncid.enabled")):
        #xbmc.log("Starting Fritzbox Client", xbmc.LOGDEBUG)
        clientPool['ncid'] = NcidClient(host=xbmcAddon.getSetting("client.ncid.host"),
                                        port=int(xbmcAddon.getSetting("client.ncid.port")),
                                        onCallIncoming=handleIncomingCall)


def bootServices():
    initServices()
    l = task.LoopingCall(shouldWeExit)
    l.start(0.5)
    reactor.run(installSignalHandlers=0)


def shouldWeExit():
    if xbmc.abortRequested == True:
        xbmc.log("shouldWeExit() - Indeed, we better stop reactor now...", xbmc.LOGDEBUG)
        reactor.stop()


if __name__ == "__main__":
    bootServices()
