#!/usr/bin/env python
# -*- coding: utf-8 -*-


from twisted.internet import reactor
from Yac.YacServer import YacServer


def handle_response(Caller):
    print "Iam into it:..!"


def test_server():
    server = YacServer(10629, handle_response)
    server.start()

    reactor.run()


if __name__ == '__main__':
    test_server()

