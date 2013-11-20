#!/usr/bin/python


import sys
import re
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


class KlicktelDe:

    def __init__(self):
        pass


    def lookupName(self, callerid):
        data = urlopen("http://www.klicktel.de/rueckwaertssuche/%s" % callerid)
        lookup = data.read().decode('utf-8')
        exp = re.compile(r">1\. (.*)</a></h4>")
        resultName = exp.search(lookup)
        if resultName != None:
            return resultName.group(1)
        else:
            return "Unknown Caller"
