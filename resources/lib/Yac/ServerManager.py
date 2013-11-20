#!/usr/bin/python

import socket, threading, thread, sys, asyncore, xbmc, xbmcgui
from time import *
from string import *

from resources.lib.Yac.ConnectionHandler import ConnectionHandler
from resources.lib.Yac.Server import Server


class ServerManager:

    def startServer(self):
        s = Server('', 10629)
        while not xbmc.abortRequested:
            asyncore.loop(timeout=1)
        s.close()