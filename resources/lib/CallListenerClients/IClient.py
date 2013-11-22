#!/usr/bin/env python

from zope.interface import Interface


class IClient(Interface):

    def __init__(self, hostname, port=1012):
        """Init the new session."""

    def connect(self):
        """Connect to Server"""

    def shutdown(self):
        """Shutdown the session."""

    def abort(self):
        """Reset session params"""
