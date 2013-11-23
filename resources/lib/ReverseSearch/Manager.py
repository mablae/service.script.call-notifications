#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
import sys, os


class Manager:
    resolverList = {}
    resultsList = []

    def __init__(self):
        self.resolverList = {}
        self.resultsList = []
        self._loadResolvers()

    def _loadResolvers(self):
        modpath = os.path.join(os.path.dirname(__file__), 'plugins')
        sys.path.insert(0, modpath)
        py_files = glob(os.path.join("./plugins", "*.py"))
        modules = [os.path.basename(f[:-3]) for f in py_files]
        for mod_name in modules:
            imported_module = __import__(mod_name, globals(), locals())
            sys.modules[mod_name] = imported_module
            self.resolverList[mod_name] = getattr(imported_module, mod_name)()

    def resolveNumber(self, number):
        self.resultsList = []
        for name, resolver in self.resolverList.iteritems():
            self.resultsList.append(resolver.findName(number))
        return self.resultsList


def test():
    mn = Manager()
    print mn.resolveNumber("042")
    print mn.resolveNumber("042641331")
    print mn.resolveNumber("042643113")
    print mn.resolveNumber("04288 392")


if __name__ == '__main__':
    test()