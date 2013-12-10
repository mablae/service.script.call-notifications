#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from urllib2 import urlopen

from PyKlicktel import klicktel

class KlicktelDeResolver():
    def findName(self, number):
        kh = klicktel.Klicktel("56cc41053cea0c9015edf960f34fe413")
        lookup = kh.invers_search(number, True).dict()["entries"][0]["displayname"]
        return lookup.encode("utf-8")
