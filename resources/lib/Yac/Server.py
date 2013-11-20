#!/usr/bin/python

import socket, threading, thread, sys, asyncore, xbmc, xbmcgui
from time import *
from string import *
from resources.lib.Yac.ConnectionHandler import ConnectionHandler


class Server(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        self.listen(1)

    def handle_accept(self):
        socket, address = self.accept()
        ConnectionHandler(socket)

    def handle_close(self):
        self.close()
