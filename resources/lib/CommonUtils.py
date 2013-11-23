#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Caller:
    caller = "Unknown"
    number = None

    def __init__(self, caller, number):
        self.caller = caller
        self.number = number

    def getDict(self):
        return {
            'caller': self.caller,
            'number': self.number
                }


class Event:
    def __init__(self):
        self.handlers = set()

    def handle(self, handler):
        self.handlers.add(handler)
        return self

    def unhandle(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self

    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)

    def getHandlerCount(self):
        return len(self.handlers)

    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__  = getHandlerCount