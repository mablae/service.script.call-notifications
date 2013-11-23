#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from urllib2 import urlopen

class KlicktelDeResolver():
    def findName(self, number):
        data = urlopen("http://www.klicktel.de/rueckwaertssuche/%s" % number)
        lookup = data.read().decode('utf-8')
        exp = re.compile(r">1\. (.*)</a></h4>")
        resultName = exp.search(lookup)
        if resultName != None:
            return resultName.group(1).encode("utf-8")
        return "Unknown"
