#!/usr/bin/python

import socket, threading, thread, sys, asyncore, xbmc, xbmcgui
from time import *
from string import *

class ConnectionHandler(asyncore.dispatcher_with_send):
    def __init__(self, notificationTime = 7000):
        self.notificationTime = notificationTime
        self.notificationIcon = "special://home/addons/script.yaclistener/phone.png"
    def handle_read(self):
        self.buffer = self.recv(1024)
        self.buffer = self.buffer[5:].split("~")
        self.close()
        global data
        if len(self.buffer) > 1:
            name = self.buffer[0]
            number = self.buffer[1]
            command = "XBMC.Notification(%s,%s,%s,%s)", name, number, self.notificationTime, self.notificationIcon
            xbmc.executebuiltin(command)
        else:
            data = self.buffer