#!/usr/bin/python 

import telnetlib
import sys


class FritzboxClient:

    host = "fritz.box"
    port = 1012
    tn = None

    def __init__(self, host, port):
        print("Started FritzboxClient...")
        self.host = host
        self.port = port
        self.tn = telnetlib.Telnet(self.port, self.port )

    def startListening(self):
        try:
            while True:
                event = self.tn.read_until( b"\n" ).decode( "utf-8" )
                edata = event.split( ';' )
                print(edata)
                if edata[1] == "RING":
                    caller = edata[3]
                    print("Incoming call from %s" % caller)

        except EOFError as eof:
            print("Connection closed by remote host.")